import json
import sqlite3
import time
from functools import wraps
from threading import RLock
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from uuid import UUID

from agent_memory.domain.models import Agent, Memory, Project, Task


SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, name TEXT NOT NULL, slug TEXT UNIQUE NOT NULL, description TEXT, metadata TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS agents (id TEXT PRIMARY KEY, name TEXT NOT NULL, provider TEXT, model TEXT, description TEXT, project_ids TEXT NOT NULL, metadata TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS memories (id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, type TEXT NOT NULL, project_id TEXT NOT NULL, agent_id TEXT, session_id TEXT, scope TEXT NOT NULL, tags TEXT NOT NULL, importance INTEGER NOT NULL, confidence REAL NOT NULL, status TEXT NOT NULL, pinned INTEGER NOT NULL, source TEXT, metadata TEXT NOT NULL, expires_at TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, FOREIGN KEY(project_id) REFERENCES projects(id));
CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
CREATE TABLE IF NOT EXISTS records (collection TEXT NOT NULL, id TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, PRIMARY KEY(collection, id));
CREATE INDEX IF NOT EXISTS idx_records_collection_created ON records(collection, created_at DESC);
CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE, agent_id TEXT REFERENCES agents(id), title TEXT NOT NULL, description TEXT NOT NULL DEFAULT '', priority TEXT NOT NULL DEFAULT 'normal' CHECK(priority IN ('low','normal','high','urgent')), status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','working','done','reopened','closed')), approved INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, completed_at TEXT);
CREATE INDEX IF NOT EXISTS idx_tasks_project_status ON tasks(project_id, status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_status ON tasks(agent_id, status, created_at DESC);
CREATE TABLE IF NOT EXISTS task_attachments (id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE, original_name TEXT NOT NULL, source_path TEXT NOT NULL, stored_path TEXT NOT NULL, mime_type TEXT, size_bytes INTEGER NOT NULL, created_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_task_attachments_task ON task_attachments(task_id, created_at);
CREATE TABLE IF NOT EXISTS task_events (id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE, actor_agent_id TEXT REFERENCES agents(id), action TEXT NOT NULL, from_status TEXT, to_status TEXT, note TEXT, created_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_task_events_task ON task_events(task_id, created_at);
"""


def _dt(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _serialize(value):
    if isinstance(value, (UUID, datetime)):
        return value.isoformat() if isinstance(value, datetime) else str(value)
    if isinstance(value, list):
        return json.dumps([_serialize(item) for item in value])
    if isinstance(value, dict):
        return json.dumps({key: _serialize(item) for key, item in value.items()})
    if isinstance(value, bool):
        return int(value)
    return value


def synchronized(method):
    """Serialize operations on the store's one shared SQLite connection."""
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapped


class SQLiteStore:
    def __init__(self, path: str = "memory.db"):
        self.path = path
        self._lock = RLock()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, timeout=30.0, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.execute("PRAGMA busy_timeout = 30000")
        # WAL allows the API's reads to continue while a desktop SQLite viewer
        # or another agent has a transaction open. Older databases may be
        # temporarily locked while switching modes, so keep startup tolerant.
        try:
            self.db.execute("PRAGMA journal_mode = WAL")
            self.db.execute("PRAGMA synchronous = NORMAL")
        except sqlite3.OperationalError as exc:
            if "locked" not in str(exc).lower():
                raise
        self.db.executescript(SCHEMA)
        self._migrate_tasks()
        if "creator_id" not in {r[1] for r in self.db.execute("PRAGMA table_info(tasks)")}:
            self.db.execute("ALTER TABLE tasks ADD COLUMN creator_id TEXT")
        self.db.execute("CREATE TABLE IF NOT EXISTS members (id TEXT PRIMARY KEY,name TEXT NOT NULL,key_hash TEXT UNIQUE NOT NULL)")
        self.db.commit()

    def _migrate_tasks(self):
        columns = {row[1] for row in self.db.execute("PRAGMA table_info(tasks)")}
        sql = self.db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tasks'").fetchone()[0]
        if "approved" in columns and "reopened" in sql and "closed" in sql:
            return
        self.db.execute("PRAGMA foreign_keys=OFF")
        self.db.execute("BEGIN IMMEDIATE")
        self.db.execute("""CREATE TABLE tasks_new (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
            agent_id TEXT REFERENCES agents(id), title TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'normal' CHECK(priority IN ('low','normal','high','urgent')),
            status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','working','done','reopened','closed')),
            approved INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, completed_at TEXT)""")
        approved = "approved" if "approved" in columns else "1"
        self.db.execute(f"INSERT INTO tasks_new SELECT id,project_id,agent_id,title,description,priority,CASE status WHEN 'pending' THEN 'open' ELSE status END,{approved},created_at,updated_at,completed_at FROM tasks")
        self.db.execute("DROP TABLE tasks")
        self.db.execute("ALTER TABLE tasks_new RENAME TO tasks")
        self.db.execute("CREATE INDEX IF NOT EXISTS idx_tasks_project_status ON tasks(project_id,status,created_at DESC)")
        self.db.execute("CREATE INDEX IF NOT EXISTS idx_tasks_agent_status ON tasks(agent_id,status,created_at DESC)")
        self.db.commit()
        self.db.execute("PRAGMA foreign_keys=ON")

    @staticmethod
    def _is_locked(error: sqlite3.OperationalError) -> bool:
        return "locked" in str(error).lower() or "busy" in str(error).lower()

    def _retry_locked(self, operation):
        """Retry short SQLite lock windows without hiding permanent failures."""
        delay = 0.1
        for attempt in range(5):
            try:
                return operation()
            except sqlite3.OperationalError as exc:
                if not self._is_locked(exc) or attempt == 4:
                    raise
                time.sleep(delay)
                delay *= 2

    def _write(self, table, entity):
        data = {k: _serialize(v) for k, v in asdict(entity).items()}
        columns = ",".join(data)
        marks = ",".join("?" for _ in data)

        def write():
            self.db.execute(f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({marks})", list(data.values()))
            self.db.commit()
            self.record_create("audit", {"action": "create", "resource": table, "resource_id": data["id"], "project_id": data.get("project_id")})
            return entity

        return self._retry_locked(write)

    @synchronized
    def create(self, entity):
        return self._write({Project: "projects", Agent: "agents", Memory: "memories"}[type(entity)], entity)

    @synchronized
    def get(self, entity_id, entity_type):
        table = {Project: "projects", Agent: "agents", Memory: "memories"}[entity_type]
        row = self.db.execute(f"SELECT * FROM {table} WHERE id=?", (str(entity_id),)).fetchone()
        return self._from_row(row, entity_type) if row else None

    @synchronized
    def by_slug(self, slug):
        row = self.db.execute("SELECT * FROM projects WHERE slug=?", (slug,)).fetchone()
        return self._from_row(row, Project) if row else None

    @synchronized
    def list(self, entity_type, **filters):
        table = {Project: "projects", Agent: "agents", Memory: "memories"}[entity_type]
        clauses, args = [], []
        for key in ("project_id", "agent_id", "session_id", "type", "scope", "status"):
            if filters.get(key) is not None:
                if entity_type is Agent and key == "project_id": clauses.append("project_ids LIKE ?"); args.append(f"%{filters[key]}%")
                else: clauses.append(f"{key}=?"); args.append(str(filters[key]))
        if filters.get("min_importance") is not None:
            clauses.append("importance>=?"); args.append(int(filters["min_importance"]))
        if filters.get("pinned") is not None:
            clauses.append("pinned=?"); args.append(int(bool(filters["pinned"])))
        if filters.get("created_after") is not None:
            clauses.append("created_at>=?"); args.append(str(filters["created_after"]))
        if filters.get("created_before") is not None:
            clauses.append("created_at<=?"); args.append(str(filters["created_before"]))
        if filters.get("tag") is not None:
            clauses.append("tags LIKE ?"); args.append(f'%"{filters["tag"]}"%')
        if filters.get("q"):
            search_columns = {Project: ["name", "slug", "description"], Agent: ["name", "model", "description"], Memory: ["title", "content", "source"]}[entity_type]
            q = f"%{filters['q']}%"
            clauses.append("(" + " OR ".join(f"{column} LIKE ?" for column in search_columns) + ")")
            args.extend([q] * len(search_columns))
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        allowed_sort = {Project: {"created_at", "updated_at", "name", "slug"}, Agent: {"created_at", "updated_at", "name"}, Memory: {"created_at", "updated_at", "importance", "confidence", "title"}}[entity_type]
        sort = filters.get("sort", "created_at"); order = str(filters.get("order", "desc")).lower()
        if sort not in allowed_sort or order not in {"asc", "desc"}: raise ValueError("Invalid sort or order")
        rows = self.db.execute(f"SELECT * FROM {table}{where} ORDER BY {sort} {order} LIMIT ? OFFSET ?", (*args, int(filters.get("limit", 20)), int(filters.get("offset", 0)))).fetchall()
        return [self._from_row(row, entity_type) for row in rows]

    @synchronized
    def update(self, entity):
        table = {Project: "projects", Agent: "agents", Memory: "memories"}[type(entity)]
        data = asdict(entity); data.pop("id")
        data = {k: _serialize(v) for k, v in data.items()}
        self.db.execute(f"UPDATE {table} SET {','.join(f'{k}=?' for k in data)} WHERE id=?", (*data.values(), str(entity.id)))
        self.db.commit()
        self.record_create("audit", {"action": "update", "resource": table, "resource_id": str(entity.id), "project_id": data.get("project_id")})
        return entity

    def _from_row(self, row, cls):
        data = dict(row)
        for key in ("metadata", "project_ids", "tags"):
            if key in data: data[key] = json.loads(data[key])
        for key in ("id", "project_id", "agent_id", "session_id"):
            if data.get(key): data[key] = UUID(data[key])
        if "project_ids" in data:
            data["project_ids"] = [UUID(value) for value in data["project_ids"]]
        for key in ("created_at", "updated_at", "expires_at"):
            if data.get(key): data[key] = datetime.fromisoformat(data[key])
        if "pinned" in data: data["pinned"] = bool(data["pinned"])
        return cls(**data)

    @synchronized
    def record_create(self, collection: str, data: dict):
        now = datetime.now().astimezone().isoformat()
        payload = dict(data)
        payload.setdefault("id", str(UUID(int=__import__("secrets").randbits(128))))
        payload.setdefault("created_at", now)
        payload.setdefault("updated_at", now)
        self.db.execute("INSERT OR REPLACE INTO records(collection,id,data,created_at,updated_at) VALUES(?,?,?,?,?)", (collection, payload["id"], json.dumps(payload, default=str), payload["created_at"], payload["updated_at"]))
        self.db.commit()
        if collection not in {"audit", "idempotency"}:
            self.record_create("audit", {"action": "create", "resource": collection, "resource_id": payload["id"], "project_id": payload.get("project_id")})
        return payload

    @synchronized
    def record_get(self, collection: str, record_id: str):
        row = self.db.execute("SELECT data FROM records WHERE collection=? AND id=?", (collection, str(record_id))).fetchone()
        return json.loads(row["data"]) if row else None

    @synchronized
    def record_list(self, collection: str, filters: dict | None = None, limit: int = 20, offset: int = 0):
        rows = self.db.execute("SELECT data FROM records WHERE collection=? ORDER BY created_at DESC", (collection,)).fetchall()
        items = [json.loads(row["data"]) for row in rows]
        filters = filters or {}
        items = [item for item in items if all(value is None or item.get(key) == str(value) or item.get(key) == value for key, value in filters.items())]
        return items[offset:offset + int(limit)]

    @synchronized
    def record_count(self, collection: str, filters: dict | None = None):
        return len(self.record_list(collection, filters, limit=10**9))

    @synchronized
    def idempotency_get(self, key: str):
        item = self.record_get("idempotency", key)
        return item.get("response") if item else None

    @synchronized
    def idempotency_record(self, key: str):
        return self.record_get("idempotency", key)

    @synchronized
    def idempotency_put(self, key: str, fingerprint: str, response):
        existing = self.record_get("idempotency", key)
        if existing and existing.get("fingerprint") != fingerprint:
            raise ValueError("Idempotency key was already used with a different payload")
        if not existing:
            self.record_create("idempotency", {"id": key, "fingerprint": fingerprint, "response": response})
        return response

    @synchronized
    def record_update(self, collection: str, record_id: str, changes: dict):
        current = self.record_get(collection, record_id)
        if not current:
            return None
        current.update(changes)
        current["updated_at"] = datetime.now().astimezone().isoformat()
        self.db.execute("UPDATE records SET data=?,updated_at=? WHERE collection=? AND id=?", (json.dumps(current, default=str), current["updated_at"], collection, str(record_id)))
        self.db.commit()
        if collection not in {"audit", "idempotency"}:
            self.record_create("audit", {"action": "update", "resource": collection, "resource_id": str(record_id), "project_id": current.get("project_id")})
        return current

    @synchronized
    def record_delete(self, collection: str, record_id: str):
        result = self.db.execute("DELETE FROM records WHERE collection=? AND id=?", (collection, str(record_id)))
        self.db.commit()
        if result.rowcount and collection != "audit":
            self.record_create("audit", {"action": "delete", "resource": collection, "resource_id": str(record_id)})
        return result.rowcount > 0

    @synchronized
    def task_create(self, task: Task):
        data = asdict(task)
        data = {key: _serialize(value) for key, value in data.items()}
        columns = ",".join(data)
        marks = ",".join("?" for _ in data)
        self.db.execute(
            f"INSERT INTO tasks ({columns}) VALUES ({marks})", list(data.values())
        )
        self.db.commit()
        self.task_event(task.id, "created", to_status=task.status)
        self.record_create(
            "audit",
            {
                "action": "create",
                "resource": "tasks",
                "resource_id": str(task.id),
                "project_id": str(task.project_id),
            },
        )
        return task

    @synchronized
    def task_get(self, task_id):
        row = self.db.execute("SELECT * FROM tasks WHERE id=?", (str(task_id),)).fetchone()
        if not row:
            return None
        data = dict(row)
        for key in ("id", "project_id", "agent_id"):
            if data.get(key):
                data[key] = UUID(data[key])
        for key in ("created_at", "updated_at", "completed_at"):
            if data.get(key):
                data[key] = datetime.fromisoformat(data[key])
        return Task(**data)

    @synchronized
    def task_list(self, *, project_id=None, agent_id=None, status=None, priority=None,
                  q=None, hide_closed=True, creator_id=None, limit=20, offset=0):
        clauses, args = [], []
        for key, value in (("project_id", project_id), ("agent_id", agent_id),
                           ("status", status), ("priority", priority)):
            if value is not None:
                clauses.append(f"{key}=?")
                args.append(str(value))
        if creator_id is not None:
            clauses.append("creator_id=?")
            args.append(creator_id)
        if hide_closed and status != "closed":
            clauses.append("status != 'closed'")
        if q:
            clauses.append("(title LIKE ? OR description LIKE ?)")
            args.extend((f"%{q}%", f"%{q}%"))
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        rows = self.db.execute(
            f"SELECT * FROM tasks{where} ORDER BY CASE priority "
            "WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 WHEN 'normal' THEN 2 ELSE 3 END, "
            "created_at DESC LIMIT ? OFFSET ?",
            (*args, int(limit), int(offset)),
        ).fetchall()
        return [self.task_get(row["id"]) for row in rows]

    @synchronized
    def task_update(self, task: Task, *, actor_agent_id=None, action="updated",
                    from_status=None, note=None):
        values = (
            str(task.project_id), str(task.agent_id) if task.agent_id else None,
            task.title, task.description, task.priority, task.status,
            int(task.approved), _dt(task.updated_at), _dt(task.completed_at), str(task.id),
        )
        self.db.execute(
            "UPDATE tasks SET project_id=?,agent_id=?,title=?,description=?,priority=?,status=?,"
            "approved=?,updated_at=?,completed_at=? WHERE id=?",
            values,
        )
        self.db.commit()
        self.task_event(
            task.id, action, actor_agent_id=actor_agent_id, from_status=from_status,
            to_status=task.status, note=note
        )
        self.record_create(
            "audit",
            {
                "action": "update",
                "resource": "tasks",
                "resource_id": str(task.id),
                "project_id": str(task.project_id),
            },
        )
        return task

    @synchronized
    def task_delete(self, task_id):
        task = self.task_get(task_id)
        if not task:
            return False
        self.db.execute("DELETE FROM tasks WHERE id=?", (str(task_id),))
        self.db.commit()
        self.record_create(
            "audit",
            {"action": "delete", "resource": "tasks", "resource_id": str(task_id),
             "project_id": str(task.project_id)},
        )
        return True

    @synchronized
    def task_event(self, task_id, action, *, actor_agent_id=None, from_status=None,
                   to_status=None, note=None):
        event_id = str(UUID(int=__import__("secrets").randbits(128)))
        created_at = datetime.now().astimezone().isoformat()
        self.db.execute(
            "INSERT INTO task_events(id,task_id,actor_agent_id,action,from_status,to_status,note,created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (event_id, str(task_id), str(actor_agent_id) if actor_agent_id else None,
             action, from_status, to_status, note, created_at),
        )
        if action != "created":
            self.db.execute(
                "UPDATE tasks SET updated_at=? WHERE id=?",
                (created_at, str(task_id)),
            )
        self.db.commit()
        return {
            "id": event_id, "task_id": str(task_id),
            "actor_agent_id": str(actor_agent_id) if actor_agent_id else None,
            "action": action, "from_status": from_status, "to_status": to_status,
            "note": note, "created_at": created_at,
        }

    @synchronized
    def task_events(self, task_id, *, limit=100, offset=0):
        rows = self.db.execute(
            "SELECT * FROM task_events WHERE task_id=? ORDER BY created_at ASC LIMIT ? OFFSET ?",
            (str(task_id), int(limit), int(offset)),
        ).fetchall()
        return [dict(row) for row in rows]

    @synchronized
    def task_add_attachment(self, task_id, attachment):
        data = dict(attachment)
        data.setdefault("created_at", datetime.now().astimezone().isoformat())
        self.db.execute(
            "INSERT INTO task_attachments(id,task_id,original_name,source_path,stored_path,mime_type,size_bytes,created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (data["id"], str(task_id), data["original_name"], data.get("source_path", data["original_name"]), data["path"],
             data.get("mime_type"), int(data["size_bytes"]), data["created_at"]),
        )
        self.db.commit()
        self.task_event(task_id, "attachment_added", note=data["original_name"])
        return {
            "id": data["id"], "task_id": str(task_id), "name": data["original_name"],
            "source_path": data.get("source_path", data["original_name"]),
            "path": data["path"], "mime_type": data.get("mime_type"),
            "size_bytes": int(data["size_bytes"]), "created_at": data["created_at"],
        }

    @synchronized
    def task_attachments(self, task_id):
        rows = self.db.execute(
            "SELECT id,task_id,original_name,source_path,stored_path,mime_type,size_bytes,created_at "
            "FROM task_attachments WHERE task_id=? ORDER BY created_at",
            (str(task_id),),
        ).fetchall()
        return [
            {"id": row["id"], "task_id": row["task_id"], "name": row["original_name"],
             "source_path": row["source_path"], "path": row["stored_path"], "mime_type": row["mime_type"],
             "size_bytes": row["size_bytes"], "created_at": row["created_at"]}
            for row in rows
        ]

    @synchronized
    def task_attachment_get(self, task_id, attachment_id):
        row = self.db.execute(
            "SELECT id,task_id,original_name,source_path,stored_path,mime_type,size_bytes,created_at "
            "FROM task_attachments WHERE task_id=? AND id=?",
            (str(task_id), str(attachment_id)),
        ).fetchone()
        if not row:
            return None
        return {"id": row["id"], "task_id": row["task_id"],
                "name": row["original_name"], "source_path": row["source_path"],
                "path": row["stored_path"],
                "mime_type": row["mime_type"], "size_bytes": row["size_bytes"],
                "created_at": row["created_at"]}


class SQLiteRepository:
    """Typed repository adapter; use cases depend on this boundary, not SQLite."""

    def __init__(self, store: SQLiteStore, entity_type):
        self.store, self.entity_type = store, entity_type

    def create(self, entity):
        return self.store.create(entity)

    def get(self, entity_id):
        return self.store.get(entity_id, self.entity_type)

    def list(self, **filters):
        return self.store.list(self.entity_type, **filters)

    def update(self, entity):
        return self.store.update(entity)

    def by_slug(self, slug):
        return self.store.by_slug(slug)


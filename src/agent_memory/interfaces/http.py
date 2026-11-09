import os
import hashlib
import json
import base64
import sqlite3
import re
from pathlib import Path
from fastapi.responses import StreamingResponse, FileResponse
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Body, Depends, File, Form, Header, HTTPException, Query, Request, UploadFile, status
from pydantic import BaseModel, ConfigDict, Field

from agent_memory.application.services import ConflictError, NotFoundError
from agent_memory.domain.models import Agent, Memory, Project, Task


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$", max_length=100)
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    provider: str | None = None
    model: str | None = None
    description: str | None = None
    project_ids: list[UUID] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryIn(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1)
    type: Literal["fact", "decision", "preference", "error", "solution", "task", "summary", "observation"]
    project_id: UUID
    agent_id: UUID | None = None
    session_id: UUID | None = None
    scope: Literal["project", "agent", "global"] = "project"
    tags: list[str] = Field(default_factory=list)
    importance: int = Field(default=5, ge=1, le=10)
    confidence: float = Field(default=1, ge=0, le=1)
    pinned: bool = False
    source: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    expires_at: Any | None = None


class TaskCreate(BaseModel):
    project_id: UUID
    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=200_000)
    priority: Literal["low", "normal", "high", "urgent"] = "normal"
    agent_id: UUID | None = None


class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=1, max_length=240)
    description: str | None = Field(default=None, max_length=200_000)
    priority: Literal["low", "normal", "high", "urgent"] | None = None
    status: Literal["open", "working", "done", "reopened", "closed"] | None = None
    agent_id: UUID | None = None
    actor_agent_id: UUID | None = None
    note: str | None = Field(default=None, max_length=4000)


class TaskEventIn(BaseModel):
    agent_id: UUID | None = None
    note: str = Field(default="", max_length=4000)


class Page(BaseModel):
    items: list[Any]
    next_cursor: str | None = None
    has_more: bool = False


def _out(value):
    if hasattr(value, "__dataclass_fields__"):
        return {k: getattr(value, k) for k in value.__dataclass_fields__}
    return value


def api_key(request: Request, x_api_key: str | None = Header(default=None)):
    dev = os.getenv("MEMORY_API_KEY", "dev-key")
    test = os.getenv("MEMORY_TEST_API_KEY", "test-key")
    store = request.app.state.store
    digest = hashlib.sha256((x_api_key or "").encode()).hexdigest()
    with store._lock:
        member = store.db.execute("SELECT id FROM members WHERE key_hash=?", (digest,)).fetchone()
    admin = dev
    loopback = bool(request.client and request.client.host in {"127.0.0.1", "::1"})
    if not x_api_key or (x_api_key not in {dev, test, admin} and not member):
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Invalid API key"})
    if x_api_key == dev and not loopback:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "dev-key is restricted to localhost"})
    request.state.api_key_role = "test" if x_api_key == test or member else "dev"
    request.state.creator_id = member[0] if member else ("builtin-test" if x_api_key == test else "dev")
    if request.state.api_key_role == "test":
        path = request.url.path
        project_read = request.method == "GET" and (path == "/v1/projects" or re.fullmatch(r"/v1/projects/[0-9a-fA-F-]+", path))
        task_create = request.method == "POST" and path == "/v1/tasks"
        task_read = request.method == "GET" and (path == "/v1/tasks" or re.fullmatch(r"/v1/tasks/[0-9a-fA-F-]+", path))
        task_update = request.method in {"PATCH", "DELETE"} and re.fullmatch(r"/v1/tasks/[0-9a-fA-F-]+", path)
        if not (project_read or task_create or task_read or task_update or (request.method == "GET" and path == "/v1/me")):
            raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "Member access is limited to projects and own tasks"})


def admin_key(x_api_key: str | None = Header(default=None)):
    expected = os.getenv("MEMORY_API_KEY", "dev-key")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "Admin access required"})


def fingerprint(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def cursor_offset(cursor: str | None) -> int:
    if not cursor: return 0
    try: return int(base64.urlsafe_b64decode(cursor.encode()).decode())
    except Exception: raise HTTPException(400, {"code": "VALIDATION_ERROR", "message": "Invalid cursor"})


def page_cursor(items: list, limit: int, offset: int) -> Page:
    has_more = len(items) > limit
    items = items[:limit]
    next_cursor = base64.urlsafe_b64encode(str(offset + limit).encode()).decode() if has_more else None
    return Page(items=items, next_cursor=next_cursor, has_more=has_more)


def build_router(store, project_service, agent_service, memory_service):
    router = APIRouter(prefix="/v1", dependencies=[Depends(api_key)])

    def task_output(task):
        result = _out(task)
        result["attachments"] = store.task_attachments(task.id)
        return result

    def get_task(task_id):
        task = store.task_get(task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        return task

    def validate_task_agent(agent_id, project_id):
        if not agent_id:
            return
        agent = store.get(agent_id, Agent)
        if not agent:
            raise HTTPException(404, "Agent not found")
        if agent.project_ids and project_id not in agent.project_ids:
            raise HTTPException(422, "Agent is not connected to this project")

    @router.get("/meta")
    def meta():
        return {"version": "0.1.0", "features": ["projects", "agents", "memories", "tasks", "task_attachments", "keyword_search"], "limits": {"max_batch": 100}}

    @router.get("/me")
    def me(request: Request):
        role = request.state.api_key_role
        allowed_tabs = (
            ["overview", "tasks", "projects", "memories", "agents", "sessions", "instructions", "audit", "members"]
            if role == "dev"
            else ["tasks", "projects"]
        )
        return {"role": role, "id": request.state.creator_id, "allowed_tabs": allowed_tabs}

    @router.get("/members")
    def members():
        with store._lock:
            return {"items": [dict(r) for r in store.db.execute("SELECT id,name FROM members")]}

    @router.post("/members", status_code=201)
    def add_member(body: dict[str, Any]):
        name = str(body.get("name", "")).strip()
        key = body.get("api_key")
        if not name or not isinstance(key, str) or len(key) < 16:
            raise HTTPException(422, "Name and an API key of at least 16 characters are required")
        if key in {os.getenv("MEMORY_API_KEY", "dev-key"), os.getenv("MEMORY_TEST_API_KEY", "test-key")}:
            raise HTTPException(409, "Key already in use")
        member_id = str(uuid4())
        try:
            with store._lock, store.db:
                store.db.execute("INSERT INTO members VALUES (?,?,?)", (member_id, name, hashlib.sha256(key.encode()).hexdigest()))
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Key already in use")
        return {"id": member_id, "name": name, "api_key": key}

    # Tasks coordinate user and agent work independently of memory records.
    @router.post("/tasks", status_code=201)
    def create_task(body: TaskCreate, request: Request):
        if not body.title.strip():
            raise HTTPException(422, "Task title cannot be blank")
        if not store.get(body.project_id, Project):
            raise HTTPException(404, "Project not found")
        validate_task_agent(body.agent_id, body.project_id)
        task = Task(**{**body.model_dump(), "title": body.title.strip(), "approved": request.state.api_key_role != "test", "creator_id": request.state.creator_id})
        return task_output(store.task_create(task))

    @router.get("/tasks", response_model=Page)
    def list_tasks(request: Request, creator_id: str | None = None, project_id: UUID | None = None, agent_id: UUID | None = None,
                   status: Literal["open", "working", "done", "reopened", "closed"] | None = None,
                   priority: Literal["low", "normal", "high", "urgent"] | None = None,
                   q: str | None = None, hide_closed: bool = True, cursor: str | None = None,
                   limit: int = Query(20, ge=1, le=100)):
        offset = cursor_offset(cursor)
        items = store.task_list(
            project_id=project_id, agent_id=agent_id, status=status, priority=priority,
            q=q, hide_closed=hide_closed, creator_id=request.state.creator_id if request.state.api_key_role == "test" else creator_id, limit=limit + 1, offset=offset,
        )
        return page_cursor([task_output(item) for item in items], limit, offset)

    @router.get("/tasks/{task_id}")
    def get_task_detail(task_id: UUID, request: Request):
        task = get_task(task_id)
        if request.state.api_key_role == "test" and task.creator_id != request.state.creator_id:
            raise HTTPException(404, "Task not found")
        return task_output(task)

    @router.patch("/tasks/{task_id}")
    def update_task(task_id: UUID, body: TaskPatch, request: Request):
        task = get_task(task_id)
        previous_status = task.status
        changes = body.model_dump(exclude_unset=True)
        if request.state.api_key_role == "test":
            if task.creator_id != request.state.creator_id:
                raise HTTPException(404, "Task not found")
            if not set(changes) <= {"title", "description", "priority", "status"}:
                raise HTTPException(403, "Members may edit only task title, description, priority and status")
            if "status" in changes and changes["status"] not in {"open", "closed", "reopened"}:
                raise HTTPException(403, "Members may set status only to open, closed or reopened")
            if any(key in changes and changes[key] != getattr(task, key) for key in ("title", "description", "priority")):
                task.approved = False
                if task.status in {"working", "done"} and "status" not in changes:
                    changes["status"] = "reopened"
        actor_agent_id = changes.pop("actor_agent_id", None)
        note = changes.pop("note", None)
        for key in ("title", "description", "priority", "status"):
            if key in changes and changes[key] is None:
                raise HTTPException(422, f"{key} cannot be null")
        if "title" in changes:
            changes["title"] = changes["title"].strip()
            if not changes["title"]:
                raise HTTPException(422, "Task title cannot be blank")
        validate_task_agent(changes.get("agent_id", task.agent_id), task.project_id)
        if not task.approved and (actor_agent_id or changes.get("status") in {"working", "done"}):
            raise HTTPException(409, "Task requires approval before work")
        if actor_agent_id:
            validate_task_agent(actor_agent_id, task.project_id)
            if task.agent_id and task.agent_id != actor_agent_id:
                raise HTTPException(409, "Task is assigned to another agent")
            if changes.get("agent_id") and changes["agent_id"] != actor_agent_id:
                raise HTTPException(409, "An agent cannot reassign a task while updating it")
            task.agent_id = actor_agent_id
            changes["agent_id"] = actor_agent_id
            if "status" not in changes and task.status in {"open", "reopened"}:
                changes["status"] = "working"
        for key, value in changes.items():
            setattr(task, key, value)
        if task.status == "done":
            if previous_status != "done" or not task.completed_at:
                task.completed_at = datetime.now(timezone.utc)
        else:
            task.completed_at = None
        task.updated_at = datetime.now(timezone.utc)
        action = "status_changed" if task.status != previous_status else "updated"
        return task_output(
            store.task_update(
                task, actor_agent_id=actor_agent_id, action=action,
                from_status=previous_status, note=note,
            )
        )

    @router.post("/tasks/{task_id}/approve")
    def approve_task(task_id: UUID, request: Request, body: dict[str, Any] = Body(default_factory=dict)):
        if request.state.api_key_role != "dev":
            raise HTTPException(403, "dev-key approval required")
        task = get_task(task_id)
        task.approved = True
        task.updated_at = datetime.now(timezone.utc)
        return task_output(store.task_update(task, action="approved", note=body.get("note", "Approved by dev-key")))

    @router.post("/tasks/{task_id}/claim")
    def claim_task(task_id: UUID, body: TaskEventIn):
        if not body.agent_id:
            raise HTTPException(422, "agent_id is required to claim a task")
        task = get_task(task_id)
        validate_task_agent(body.agent_id, task.project_id)
        if not task.approved:
            raise HTTPException(409, "Task requires dev-key approval before an agent can claim it")
        if task.agent_id and task.agent_id != body.agent_id:
            raise HTTPException(409, "Task is assigned to another agent")
        previous_status = task.status
        task.agent_id = body.agent_id
        task.status = "working"
        task.completed_at = None
        task.updated_at = datetime.now(timezone.utc)
        return task_output(
            store.task_update(
                task, actor_agent_id=body.agent_id, action="claimed",
                from_status=previous_status, note=body.note,
            )
        )

    @router.post("/tasks/{task_id}/events", status_code=201)
    def add_task_event(task_id: UUID, body: TaskEventIn):
        if not body.note.strip():
            raise HTTPException(422, "Update note cannot be blank")
        task = get_task(task_id)
        if body.agent_id:
            validate_task_agent(body.agent_id, task.project_id)
            if task.agent_id and task.agent_id != body.agent_id:
                raise HTTPException(409, "Task is assigned to another agent")
        event = store.task_event(
            task.id, "commented", actor_agent_id=body.agent_id,
            from_status=task.status, to_status=task.status, note=body.note,
        )
        return event

    @router.get("/tasks/{task_id}/events", response_model=Page)
    def list_task_events(task_id: UUID, cursor: str | None = None,
                         limit: int = Query(50, ge=1, le=100)):
        get_task(task_id)
        offset = cursor_offset(cursor)
        events = store.task_events(task_id, limit=limit + 1, offset=offset)
        return page_cursor(events, limit, offset)

    @router.post("/tasks/{task_id}/attachments", status_code=201)
    async def add_task_attachments(task_id: UUID, files: list[UploadFile] = File(...),
                                   source_paths: list[str] | None = Form(default=None)):
        get_task(task_id)
        if len(files) > 20:
            raise HTTPException(413, "A task can receive at most 20 files per upload")
        base = Path(os.getenv("MEMORY_ATTACHMENT_DIR", str(Path(store.path).resolve().parent / "attachments"))).resolve()
        directory = (base / "tasks" / str(task_id)).resolve()
        if not directory.is_relative_to(base):
            raise HTTPException(400, "Invalid attachment path")
        directory.mkdir(parents=True, exist_ok=True)
        source_paths = source_paths or []
        payloads = []
        total_size = 0
        for index, upload in enumerate(files):
            payload = await upload.read(25 * 1024 * 1024 + 1)
            if len(payload) > 25 * 1024 * 1024:
                raise HTTPException(413, "Each attachment must be 25 MB or smaller")
            total_size += len(payload)
            if total_size > 100 * 1024 * 1024:
                raise HTTPException(413, "Combined attachments must be 100 MB or smaller")
            payloads.append((index, upload, payload))
        created = []
        for index, upload, payload in payloads:
            original_name = Path(upload.filename or "attachment").name
            safe_name = re.sub(r"[^A-Za-z0-9._ -]", "_", original_name).strip(" .")[:160]
            safe_name = safe_name or "attachment"
            attachment_id = str(uuid4())
            target = (directory / f"{attachment_id}-{safe_name}").resolve()
            if not target.is_relative_to(base):
                raise HTTPException(400, "Invalid attachment filename")
            target.write_bytes(payload)
            source_path = source_paths[index] if index < len(source_paths) else original_name
            created.append(store.task_add_attachment(task_id, {
                "id": attachment_id, "original_name": original_name,
                "source_path": source_path, "path": str(target),
                "mime_type": upload.content_type, "size_bytes": len(payload),
            }))
        return {"items": created}

    @router.get("/tasks/{task_id}/attachments/{attachment_id}/download")
    def download_task_attachment(task_id: UUID, attachment_id: UUID):
        get_task(task_id)
        attachment = store.task_attachment_get(task_id, attachment_id)
        if not attachment:
            raise HTTPException(404, "Attachment not found")
        base = Path(os.getenv("MEMORY_ATTACHMENT_DIR", str(Path(store.path).resolve().parent / "attachments"))).resolve()
        target = Path(attachment["path"]).resolve()
        if not target.is_relative_to(base) or not target.is_file():
            raise HTTPException(404, "Attachment file not found")
        return FileResponse(
            target, filename=attachment["name"],
            media_type=attachment["mime_type"] or "application/octet-stream",
        )

    @router.delete("/tasks/{task_id}")
    def delete_task(task_id: UUID, request: Request):
        task = get_task(task_id)
        if request.state.api_key_role == "test" and task.creator_id != request.state.creator_id:
            raise HTTPException(404, "Task not found")
        attachments = store.task_attachments(task_id)
        if not store.task_delete(task_id):
            raise HTTPException(404, "Task not found")
        base = Path(os.getenv("MEMORY_ATTACHMENT_DIR", str(Path(store.path).resolve().parent / "attachments"))).resolve()
        for attachment in attachments:
            target = Path(attachment["path"]).resolve()
            if target.is_relative_to(base):
                target.unlink(missing_ok=True)
        return {"deleted": True, "id": str(task_id)}

    @router.post("/projects", status_code=201)
    def create_project(body: ProjectIn):
        try: return _out(project_service.create(Project(**body.model_dump())))
        except ConflictError as exc: raise HTTPException(409, str(exc)) from exc
        except sqlite3.OperationalError as exc:
            if "locked" in str(exc).lower() or "busy" in str(exc).lower():
                raise HTTPException(503, {"code": "DATABASE_BUSY", "message": "Memory database is busy; retry shortly"}) from exc
            raise

    @router.get("/projects", response_model=Page)
    def list_projects(q: str | None = None, sort="created_at", order="desc", cursor: str | None = None, limit: int = Query(20, ge=1, le=100)):
        try: return typed_page(Project, {"q": q, "sort": sort, "order": order}, limit, cursor)
        except ValueError as exc: raise HTTPException(400, str(exc)) from exc

    @router.get("/projects/{project_id}")
    def get_project(project_id: UUID):
        try: return _out(project_service.get(project_id))
        except NotFoundError as exc: raise HTTPException(404, str(exc)) from exc
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc

    @router.post("/agents", status_code=201)
    def create_agent(body: AgentIn): return _out(agent_service.create(Agent(**body.model_dump())))

    @router.get("/agents", response_model=Page)
    def list_agents(project_id: UUID | None = None, q: str | None = None, status: str | None = None, sort="created_at", order="desc", cursor: str | None = None, limit: int = Query(20, ge=1, le=100)):
        try: return typed_page(Agent, {"project_id": project_id, "q": q, "status": status, "sort": sort, "order": order}, limit, cursor)
        except ValueError as exc: raise HTTPException(400, str(exc)) from exc

    @router.get("/agents/{agent_id}")
    def get_agent(agent_id: UUID):
        try: return _out(agent_service.get(agent_id))
        except NotFoundError as exc: raise HTTPException(404, str(exc)) from exc

    @router.post("/memories", status_code=201)
    def create_memory(body: MemoryIn, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
        try:
            if idempotency_key:
                prior = store.idempotency_record(idempotency_key)
                if prior:
                    if prior["fingerprint"] != fingerprint(body.model_dump()): raise HTTPException(409, "Idempotency key was already used with a different payload")
                    return prior["response"]
            result = _out(memory_service.create(Memory(**body.model_dump())))
            if idempotency_key: store.idempotency_put(idempotency_key, fingerprint(body.model_dump()), result)
            return result
        except NotFoundError as exc: raise HTTPException(404, str(exc)) from exc
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc

    @router.get("/memories", response_model=Page)
    def list_memories(project_id: UUID | None = None, agent_id: UUID | None = None, session_id: UUID | None = None, type: str | None = None, scope: str | None = None, status: str | None = None, tag: str | None = None, pinned: bool | None = None, min_importance: int | None = Query(None, ge=1, le=10), created_after: str | None = None, created_before: str | None = None, q: str | None = None, sort="created_at", order="desc", cursor: str | None = None, limit: int = Query(20, ge=1, le=100)):
        try: return typed_page(Memory, {"project_id": project_id, "agent_id": agent_id, "session_id": session_id, "type": type, "scope": scope, "status": status, "tag": tag, "pinned": pinned, "min_importance": min_importance, "created_after": created_after, "created_before": created_before, "q": q, "sort": sort, "order": order}, limit, cursor)
        except ValueError as exc: raise HTTPException(400, str(exc)) from exc

    @router.get("/memories/search", response_model=Page)
    def search_memories(q: str = Query(min_length=1), project_id: UUID | None = None, agent_id: UUID | None = None, type: str | None = None, tag: str | None = None, min_importance: int | None = Query(None, ge=1, le=10), include_archived: bool = False, limit: int = Query(20, ge=1, le=100), cursor: str | None = None):
        return typed_page(Memory, {"q": q, "project_id": project_id, "agent_id": agent_id, "type": type, "tag": tag, "min_importance": min_importance, "status": None if include_archived else "active", "sort": "created_at", "order": "desc"}, limit, cursor)

    @router.post("/memories/search", response_model=Page)
    def search_memories_body(body: dict = Body(...)):
        if body.get("mode", "keyword") != "keyword" or not body.get("query") or not 1 <= body.get("limit", 20) <= 100: raise HTTPException(422, "Only keyword search with limit 1..100 is supported")
        filters = body.get("filters", {})
        items = store.list(Memory, q=body.get("query", ""), project_id=filters.get("project_id"), agent_id=filters.get("agent_id"), type=(filters.get("types") or [None])[0], tag=(filters.get("tags") or [None])[0], min_importance=filters.get("min_importance"), created_after=filters.get("created_after"), limit=body.get("limit", 20))
        return Page(items=[_out(x) for x in items])

    @router.get("/memories/{memory_id}")
    def get_memory(memory_id: UUID):
        try: return _out(memory_service.get(memory_id))
        except NotFoundError as exc: raise HTTPException(404, str(exc)) from exc

    @router.post("/memories/{memory_id}/archive")
    def archive_memory(memory_id: UUID):
        try: return _out(memory_service.archive(memory_id))
        except NotFoundError as exc: raise HTTPException(404, str(exc)) from exc

    def record(collection, record_id=None):
        return store.record_get(collection, str(record_id)) if record_id else None

    def page(collection, filters=None, limit=20, cursor=None):
        offset = cursor_offset(cursor)
        return page_cursor(store.record_list(collection, filters, limit=limit + 1, offset=offset), limit, offset)

    def typed_page(entity_type, filters, limit, cursor):
        offset = cursor_offset(cursor)
        items = store.list(entity_type, **filters, limit=limit + 1, offset=offset)
        return page_cursor([_out(item) for item in items], limit, offset)

    # Projects and agents: remaining lifecycle operations.
    @router.patch("/projects/{project_id}")
    def update_project(project_id: UUID, body: dict = Body(...)):
        project = project_service.get(project_id)
        for key in ("name", "description", "metadata", "status"):
            if key in body: setattr(project, key, body[key])
        return _out(store.update(project))

    @router.delete("/projects/{project_id}")
    def delete_project(project_id: UUID, hard: bool = False):
        project_service.get(project_id)
        project = store.get(project_id, Project)
        if hard:
            attachments = [
                attachment
                for task in store.task_list(project_id=project_id, limit=100000)
                for attachment in store.task_attachments(task.id)
            ]
            store.db.execute("DELETE FROM memories WHERE project_id=?", (str(project_id),)); store.db.execute("DELETE FROM projects WHERE id=?", (str(project_id),)); store.db.commit()
            attachment_root = Path(os.getenv("MEMORY_ATTACHMENT_DIR", str(Path(store.path).resolve().parent / "attachments"))).resolve()
            for attachment in attachments:
                path = Path(attachment["path"]).resolve()
                if path.is_relative_to(attachment_root):
                    path.unlink(missing_ok=True)
        else: project.status = "deleted"; store.update(project)
        return {"deleted": True, "id": str(project_id), "hard": hard}

    @router.patch("/agents/{agent_id}")
    def update_agent(agent_id: UUID, body: dict = Body(...)):
        agent = agent_service.get(agent_id)
        for key in ("name", "model", "description", "project_ids", "metadata", "status"):
            if key in body: setattr(agent, key, body[key])
        return _out(store.update(agent))

    @router.delete("/agents/{agent_id}")
    def delete_agent(agent_id: UUID):
        agent_service.get(agent_id)
        agent = store.get(agent_id, Agent); agent.status = "deleted"; store.update(agent)
        return {"deleted": True, "id": str(agent_id)}

    # Instructions are stored as policy records and are only eligible for context when approved.
    @router.post("/instructions", status_code=201)
    def create_instruction(body: dict = Body(...)):
        required = ("title", "content", "scope", "priority", "source", "status")
        if any(key not in body for key in required): raise HTTPException(422, "Missing instruction fields")
        if body["scope"] not in ("global", "project", "agent") or not 0 <= body["priority"] <= 100: raise HTTPException(422, "Invalid instruction fields")
        if body["scope"] == "project" and (not body.get("project_id") or not store.get(body["project_id"], Project)): raise HTTPException(404, "Project not found")
        if body["scope"] == "agent" and (not body.get("agent_id") or not store.get(body["agent_id"], Agent)): raise HTTPException(404, "Agent not found")
        return store.record_create("instructions", body)

    @router.get("/instructions", response_model=Page)
    def list_instructions(scope=None, project_id=None, agent_id=None, status=None, tag=None, q=None, cursor: str | None = None, limit: int = Query(20, ge=1, le=100)):
        offset = cursor_offset(cursor)
        items = store.record_list("instructions", {"scope": scope, "project_id": project_id, "agent_id": agent_id, "status": status}, limit + 1, offset)
        if tag: items = [x for x in items if tag in x.get("tags", [])]
        if q: items = [x for x in items if q.lower() in (x.get("title", "") + x.get("content", "")).lower()]
        return page_cursor(items, limit, offset)

    @router.get("/instructions/{instruction_id}")
    def get_instruction(instruction_id: UUID):
        item = record("instructions", instruction_id)
        if not item: raise HTTPException(404, "Instruction not found")
        return item

    @router.patch("/instructions/{instruction_id}")
    def update_instruction(instruction_id: UUID, body: dict = Body(...)):
        if not record("instructions", instruction_id): raise HTTPException(404, "Instruction not found")
        return store.record_update("instructions", instruction_id, {k: body[k] for k in ("title", "content", "priority", "tags", "expires_at") if k in body})

    def _instruction_action(instruction_id: UUID, action: str, body: dict):
        if not record("instructions", instruction_id): raise HTTPException(404, "Instruction not found")
        return store.record_update("instructions", instruction_id, {"status": "approved" if action == "approve" else "revoked", "reason": body.get("reason")})

    @router.post("/instructions/{instruction_id}/approve", dependencies=[Depends(admin_key)])
    def approve_instruction(instruction_id: UUID, body: dict = Body(default={})): return _instruction_action(instruction_id, "approve", body)

    @router.post("/instructions/{instruction_id}/revoke", dependencies=[Depends(admin_key)])
    def revoke_instruction(instruction_id: UUID, body: dict = Body(default={})): return _instruction_action(instruction_id, "revoke", body)

    @router.delete("/instructions/{instruction_id}")
    def delete_instruction(instruction_id: UUID):
        if not store.record_delete("instructions", instruction_id): raise HTTPException(404, "Instruction not found")
        return {"deleted": True, "id": str(instruction_id)}

    # Memory lifecycle, revisions, links and feedback.
    @router.post("/memories/batch", status_code=201)
    def batch_memories(body: dict = Body(...), atomic: bool = True):
        items = body.get("items", [])
        if not 1 <= len(items) <= 100: raise HTTPException(422, "items must contain 1..100 memories")
        created = []
        try:
            for item in items: created.append(_out(memory_service.create(Memory(**MemoryIn.model_validate(item).model_dump()))))
        except Exception:
            if atomic: raise HTTPException(422, "Batch validation failed")
        return {"items": created}

    @router.patch("/memories/{memory_id}")
    def update_memory(memory_id: UUID, body: dict = Body(...)):
        memory = memory_service.get(memory_id)
        store.record_create("memory_revisions", {"memory_id": str(memory_id), "snapshot": _out(memory)})
        for key in ("title", "content", "type", "tags", "importance", "confidence", "pinned", "metadata", "expires_at"):
            if key in body: setattr(memory, key, body[key])
        memory.updated_at = datetime.now(timezone.utc)
        return _out(store.update(memory))

    @router.delete("/memories/{memory_id}")
    def delete_memory(memory_id: UUID, hard: bool = False):
        memory = memory_service.get(memory_id)
        if hard: store.db.execute("DELETE FROM memories WHERE id=?", (str(memory_id),)); store.db.commit()
        else: memory.status = "archived"; store.update(memory)
        return {"deleted": True, "id": str(memory_id), "hard": hard}

    @router.post("/memories/{memory_id}/feedback", status_code=201)
    def memory_feedback(memory_id: UUID, body: dict = Body(...)):
        memory_service.get(memory_id)
        if body.get("rating") not in ("useful", "irrelevant", "incorrect", "outdated"):
            raise HTTPException(422, "Invalid feedback rating")
        return store.record_create("memory_feedback", {**body, "memory_id": str(memory_id)})

    @router.get("/memories/{memory_id}/revisions", response_model=Page)
    def memory_revisions(memory_id: UUID, limit: int = Query(20, ge=1, le=100), cursor: str | None = None):
        memory_service.get(memory_id); return page("memory_revisions", {"memory_id": memory_id}, limit, cursor)

    @router.get("/memories/{memory_id}/links", response_model=Page)
    def memory_links(memory_id: UUID, relation: str | None = None, limit: int = Query(20, ge=1, le=100), cursor: str | None = None):
        memory_service.get(memory_id); return page("memory_links", {"memory_id": memory_id, "relation": relation}, limit, cursor)

    @router.post("/memories/{memory_id}/links", status_code=201)
    def create_memory_link(memory_id: UUID, body: dict = Body(...)):
        memory_service.get(memory_id)
        if body.get("relation") not in ("related", "supports", "contradicts", "derived_from"): raise HTTPException(422, "Invalid link relation")
        memory_service.get(UUID(body["target_memory_id"]))
        return store.record_create("memory_links", {**body, "memory_id": str(memory_id)})

    @router.delete("/memories/{memory_id}/links/{link_id}")
    def delete_memory_link(memory_id: UUID, link_id: UUID):
        memory_service.get(memory_id)
        if not store.record_delete("memory_links", link_id): raise HTTPException(404, "Link not found")
        return {"deleted": True, "id": str(link_id)}

    def _memory_action(memory_id: UUID, action: str, body: dict):
        memory = memory_service.get(memory_id)
        if action == "restore": memory.status = "active"
        elif action == "pin": memory.pinned = body.get("pinned", True)
        elif action == "supersede":
            memory_service.get(UUID(body["replacement_memory_id"])); memory.status = "superseded"; memory.metadata["replacement_memory_id"] = body.get("replacement_memory_id")
        return _out(store.update(memory))

    @router.post("/memories/{memory_id}/restore")
    def restore_memory(memory_id: UUID, body: dict = Body(default={})): return _memory_action(memory_id, "restore", body)

    @router.post("/memories/{memory_id}/pin")
    def pin_memory(memory_id: UUID, body: dict = Body(...)): return _memory_action(memory_id, "pin", body)

    @router.post("/memories/{memory_id}/supersede")
    def supersede_memory(memory_id: UUID, body: dict = Body(...)): return _memory_action(memory_id, "supersede", body)

    # Sessions, events and summaries.
    @router.post("/sessions", status_code=201)
    def create_session(body: dict = Body(...)):
        if not body.get("project_id") or not store.get(body["project_id"], Project): raise HTTPException(404, "Project not found")
        if body.get("agent_id") and not store.get(body["agent_id"], Agent): raise HTTPException(404, "Agent not found")
        return store.record_create("sessions", {**body, "status": "active"})

    @router.get("/sessions", response_model=Page)
    def list_sessions(project_id=None, agent_id=None, status=None, started_after=None, started_before=None, limit: int = Query(20, ge=1, le=100), cursor: str | None = None):
        result = page("sessions", {"project_id": project_id, "agent_id": agent_id, "status": status}, limit, cursor)
        if started_after or started_before: result.items = [item for item in result.items if (not started_after or item.get("created_at", "") >= started_after) and (not started_before or item.get("created_at", "") <= started_before)]
        return result

    @router.get("/sessions/{session_id}")
    def get_session(session_id: UUID):
        item = record("sessions", session_id)
        if not item: raise HTTPException(404, "Session not found")
        return item

    @router.patch("/sessions/{session_id}")
    def update_session(session_id: UUID, body: dict = Body(...)):
        if not record("sessions", session_id): raise HTTPException(404, "Session not found")
        return store.record_update("sessions", session_id, body)

    @router.post("/sessions/{session_id}/close")
    def close_session(session_id: UUID, body: dict = Body(...)):
        if not record("sessions", session_id): raise HTTPException(404, "Session not found")
        if body.get("status") not in ("completed", "failed", "cancelled"): raise HTTPException(422, "Invalid session status")
        return store.record_update("sessions", session_id, {**body, "ended_at": body.get("ended_at", datetime.now(timezone.utc).isoformat())})

    @router.post("/sessions/{session_id}/events", status_code=201)
    def create_event(session_id: UUID, body: dict = Body(...), idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
        if not record("sessions", session_id): raise HTTPException(404, "Session not found")
        if body.get("role") not in ("user", "assistant", "tool", "system") or body.get("kind") not in ("message", "tool_call", "tool_result", "file_change", "checkpoint", "error") or not body.get("content"): raise HTTPException(422, "Invalid event")
        if idempotency_key:
            prior = store.idempotency_record(idempotency_key)
            if prior:
                if prior["fingerprint"] != fingerprint(body): raise HTTPException(409, "Idempotency key was already used with a different payload")
                return prior["response"]
        result = store.record_create("events", {**body, "session_id": str(session_id)})
        if idempotency_key: store.idempotency_put(idempotency_key, fingerprint(body), result)
        return result

    @router.post("/sessions/{session_id}/events/batch", status_code=201)
    def create_events(session_id: UUID, body: dict = Body(...)):
        if not record("sessions", session_id): raise HTTPException(404, "Session not found")
        events = body.get("events", [])
        if not 1 <= len(events) <= 100: raise HTTPException(422, "events must contain 1..100 items")
        for event in events:
            if event.get("role") not in ("user", "assistant", "tool", "system") or event.get("kind") not in ("message", "tool_call", "tool_result", "file_change", "checkpoint", "error") or not event.get("content"): raise HTTPException(422, "Invalid event")
        return {"items": [store.record_create("events", {**event, "session_id": str(session_id)}) for event in events]}

    @router.get("/sessions/{session_id}/events", response_model=Page)
    def list_events(session_id: UUID, role=None, kind=None, after_sequence: int | None = None, before_sequence: int | None = None, limit: int = Query(20, ge=1, le=100), cursor: str | None = None, order="asc"):
        if not record("sessions", session_id): raise HTTPException(404, "Session not found")
        result = page("events", {"session_id": session_id, "role": role, "kind": kind}, limit, cursor)
        if after_sequence is not None: result.items = [item for item in result.items if item.get("sequence", 0) > after_sequence]
        if before_sequence is not None: result.items = [item for item in result.items if item.get("sequence", 0) < before_sequence]
        if order == "asc": result.items.reverse()
        return result

    @router.get("/sessions/{session_id}/summary")
    def get_summary(session_id: UUID):
        item = next(iter(store.record_list("summaries", {"session_id": session_id}, 1)), None)
        if not item: raise HTTPException(404, "Summary not found")
        return item

    @router.put("/sessions/{session_id}/summary")
    def put_summary(session_id: UUID, body: dict = Body(...)):
        existing = next(iter(store.record_list("summaries", {"session_id": session_id}, 1)), None)
        return store.record_update("summaries", existing["id"], body) if existing else store.record_create("summaries", {**body, "session_id": str(session_id)})

    @router.get("/events/search", response_model=Page)
    def search_events(q: str = Query(min_length=1), project_id=None, agent_id=None, session_id=None, kind=None, from_: str | None = Query(None, alias="from"), to: str | None = None, limit: int = Query(20, ge=1, le=100), cursor: str | None = None):
        items = store.record_list("events", {"project_id": project_id, "agent_id": agent_id, "session_id": session_id, "kind": kind}, limit + 1, cursor_offset(cursor))
        items = [item for item in items if q.lower() in str(item.get("content", "")).lower() and (not from_ or item.get("created_at", "") >= from_) and (not to or item.get("created_at", "") <= to)]
        return page_cursor(items, limit, cursor_offset(cursor))

    # Context, stats, audit, maintenance and portability endpoints.
    @router.post("/context")
    def context(body: dict = Body(...), preview: bool = False):
        if not 256 <= body.get("max_tokens", 0) <= 16000 or not 1 <= body.get("limit_memories", 0) <= 100:
            raise HTTPException(422, "max_tokens must be 256..16000 and limit_memories must be 1..100")
        if not body.get("project_id") or not store.get(body["project_id"], Project): raise HTTPException(404, "Project not found")
        task_terms = set((body.get("query") or body.get("task") or "").lower().split())
        memories = store.list(Memory, project_id=body.get("project_id"), agent_id=body.get("agent_id"), status="active", limit=10000)
        types, tags = set(body.get("types") or []), set(body.get("tags") or [])
        excluded = {str(value) for value in body.get("exclude_memory_ids", [])}
        candidates = []
        for memory in memories:
            if str(memory.id) in excluded or (types and memory.type not in types) or (tags and not tags.intersection(memory.tags)) or (body.get("min_importance") and memory.importance < body["min_importance"]): continue
            words = set((memory.title + " " + memory.content + " " + " ".join(memory.tags)).lower().split())
            score = len(task_terms.intersection(words)) + memory.importance / 10
            candidates.append((score, _out(memory)))
        candidates.sort(key=lambda item: item[0], reverse=True)
        selected = [item for _, item in candidates[:body.get("limit_memories", 12)]]
        instructions = []
        if body.get("include_instructions", True):
            for item in store.record_list("instructions", {"status": "approved"}, 1000):
                if item.get("scope") == "global" or (item.get("scope") == "project" and item.get("project_id") == str(body.get("project_id"))) or (item.get("scope") == "agent" and item.get("agent_id") == str(body.get("agent_id"))):
                    instructions.append({"id": item["id"], "content": item["content"], "priority": item.get("priority", 0), "scope": item["scope"]})
        instructions.sort(key=lambda item: item["priority"], reverse=True)
        memory_items = [{**item, "score": 1.0, "reason": "keyword/project match"} for item in selected]
        token_estimate = sum(len(str(item.get("content", "")).split()) for item in memory_items + instructions)
        result = {"project_id": body.get("project_id"), "agent_id": body.get("agent_id"), "task": body.get("task"), "token_estimate": token_estimate, "truncated": token_estimate > body.get("max_tokens", 16000), "instructions": instructions, "memories": memory_items}
        session_id = body.get("session_id")
        if body.get("include_session_summary", True) and session_id:
            result["session_summary"] = next(iter(store.record_list("summaries", {"session_id": session_id}, 1)), None)
        if body.get("include_recent_events") and session_id:
            result["recent_events"] = store.record_list("events", {"session_id": session_id}, 20)
        if body.get("format") == "markdown": result["rendered_markdown"] = "\n".join(f"## {item['title']}\n{item['content']}" for item in result["memories"])
        return result

    @router.post("/context/preview")
    def context_preview(body: dict = Body(...)): return {**context(body, preview=True), "diagnostics": {"strategy": "keyword"}}

    @router.post("/context/feedback", status_code=201)
    def context_feedback(body: dict = Body(...)): return store.record_create("context_feedback", body)

    @router.get("/stats")
    def stats(project_id=None, agent_id=None, from_: str | None = Query(None, alias="from"), to: str | None = None):
        memory_filters = {"project_id": project_id, "agent_id": agent_id, "created_after": from_, "created_before": to}
        record_filters = {"project_id": project_id, "agent_id": agent_id}
        storage_path = getattr(store, "path", None)
        return {"memories": len(store.list(Memory, limit=100000, **memory_filters)), "sessions": len(store.record_list("sessions", record_filters, 100000)), "events": len(store.record_list("events", record_filters, 100000)), "instructions": len(store.record_list("instructions", record_filters, 100000)), "storage_bytes": Path(storage_path).stat().st_size if storage_path and Path(storage_path).exists() else 0}

    @router.get("/audit", response_model=Page)
    def audit(limit: int = Query(20, ge=1, le=100), cursor: str | None = None, project_id=None, actor_id=None, action=None): return page("audit", {"project_id": project_id, "actor_id": actor_id, "action": action}, limit, cursor)

    @router.post("/maintenance/expire")
    def expire(body: dict = Body(default={}), dry_run: bool = True):
        before = body.get("before") or datetime.now(timezone.utc).isoformat()
        candidates = [item for item in store.list(Memory, project_id=body.get("project_id"), limit=100000) if item.expires_at and item.expires_at.isoformat() <= before and item.status == "active"]
        if not dry_run:
            for item in candidates: item.status = "archived"; store.update(item)
        return {"dry_run": dry_run, "expired": len(candidates), "memory_ids": [str(item.id) for item in candidates]}

    @router.post("/maintenance/deduplicate")
    def deduplicate(body: dict = Body(...), dry_run: bool = True):
        memories = store.list(Memory, project_id=body.get("project_id"), limit=100000)
        seen, duplicates = {}, []
        for item in memories:
            key = (item.title.strip().lower(), item.content.strip().lower())
            if key in seen: duplicates.append({"duplicate_id": str(item.id), "canonical_id": seen[key]})
            else: seen[key] = str(item.id)
        if not dry_run:
            for duplicate in duplicates:
                item = memory_service.get(UUID(duplicate["duplicate_id"])); item.status = "superseded"; store.update(item)
        return {"dry_run": dry_run, "duplicates": duplicates, "threshold": body.get("threshold", 0.95), "rule": "exact normalized title and content"}

    @router.post("/export")
    def export_data(body: dict = Body(...)):
        project_id = body.get("project_id")
        if not project_id or not store.get(project_id, Project): raise HTTPException(404, "Project not found")
        if body.get("format", "jsonl") != "jsonl": raise HTTPException(422, "Only jsonl export is supported")
        memories = store.list(Memory, project_id=project_id, limit=100000)
        sessions = store.record_list("sessions", {"project_id": project_id}, 100000) if body.get("include_events", True) else []
        events = [event for session in sessions for event in store.record_list("events", {"session_id": session.get("id")}, 100000)]
        records = [{"record_type": "memory", **_out(item)} for item in memories] + [{"record_type": "session", **item} for item in sessions] + [{"record_type": "event", **item} for item in events]
        if body.get("include_audit"): records.extend({"record_type": "audit", **item} for item in store.record_list("audit", {"project_id": project_id}, 100000))
        payload = "".join(json.dumps(item, default=str) + "\n" for item in records)
        return StreamingResponse(iter([payload]), media_type="application/x-ndjson", headers={"Content-Disposition": "attachment; filename=agent-memory-export.jsonl"})

    @router.post("/import")
    async def import_data(request: Request):
        if request.headers.get("content-type", "").startswith("multipart/"):
            form = await request.form()
            upload = form.get("file")
            raw = (await upload.read()).decode() if upload else ""
            body = {"jsonl": raw, "project_id": form.get("project_id"), "dry_run": str(form.get("dry_run", "false")).lower() == "true"}
        else:
            body = await request.json()
        raw_items = body.get("items")
        if raw_items is None and body.get("jsonl"):
            raw_items = [json.loads(line) for line in body["jsonl"].splitlines() if line.strip()]
        raw_items = raw_items or []
        if not body.get("project_id"): raise HTTPException(422, "project_id is required")
        if len(raw_items) > 10000: raise HTTPException(413, "Import exceeds the 10000-record limit")
        errors, imported, validated = [], 0, []
        for item in raw_items:
            try:
                if item.get("record_type") == "memory": validated.append(("memory", Memory(**MemoryIn.model_validate({k: v for k, v in item.items() if k != "record_type"}).model_dump())))
                else: validated.append((item.get("record_type", "imported"), item))
            except Exception as exc: errors.append({"record": item, "message": str(exc)})
        if errors: return {"dry_run": body.get("dry_run", False), "imported": 0, "errors": errors}
        if not body.get("dry_run", False):
            for collection, item in validated:
                if collection == "memory": memory_service.create(item)
                else: store.record_create(collection, item)
                imported += 1
        else: imported = len(validated)
        return {"dry_run": body.get("dry_run", False), "imported": imported, "errors": errors}

    @router.post("/admin/backup", dependencies=[Depends(admin_key)])
    def backup(body: dict = Body(default={} )):
        backup_dir = Path(os.getenv("MEMORY_BACKUP_DIR", "backups")).resolve()
        backup_dir.mkdir(parents=True, exist_ok=True)
        requested = Path(body.get("destination", "agent-memory.sqlite3")).name
        destination = (backup_dir / requested).resolve()
        if backup_dir not in destination.parents: raise HTTPException(400, "Invalid backup destination")
        target = sqlite3.connect(destination)
        try: store.db.backup(target)
        finally: target.close()
        return store.record_create("backups", {"destination": str(destination), "status": "completed"})

    @router.get("/admin/backups", response_model=Page, dependencies=[Depends(admin_key)])
    def backups(limit: int = Query(20, ge=1, le=100), cursor: str | None = None): return page("backups", limit=limit, cursor=cursor)

    return router


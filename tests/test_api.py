import io
import json
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from agent_memory.domain.models import Memory, Project
from agent_memory.infrastructure.sqlite import SQLiteStore
from agent_memory.main import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_API_KEY", "dev-key")
    monkeypatch.setenv("MEMORY_ADMIN_API_KEY", "dev-key")
    return TestClient(create_app(SQLiteStore(str(tmp_path / "memory.db"))), client=("127.0.0.1", 1234))


def headers(key="dev-key"):
    return {"X-API-Key": key}


def seed(client):
    project = client.post("/v1/projects", headers=headers(), json={"name": "Demo", "slug": "demo"}).json()
    agent = client.post("/v1/agents", headers=headers(), json={"name": "Agent", "project_ids": [project["id"]]}).json()
    memory = client.post("/v1/memories", headers=headers(), json={"title": "Decision", "content": "Use SQLite", "type": "decision", "project_id": project["id"], "agent_id": agent["id"]}).json()
    return project, agent, memory


def test_auth_health_docs_and_error_envelope(client):
    assert client.get("/health").json() == {"status": "ok", "db": "ok"}
    assert client.get("/v1/meta").status_code == 401
    response = client.get("/v1/meta", headers=headers())
    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    error = client.get("/v1/projects/not-a-uuid", headers=headers()).json()["error"]
    assert error["request_id"]
    assert client.get("/docs").status_code == 200
    assert len(client.get("/openapi.json").json()["paths"]) >= 46


def test_projects_agents_and_memories_lifecycle(client):
    project, agent, memory = seed(client)
    assert client.patch(f"/v1/projects/{project['id']}", headers=headers(), json={"description": "updated"}).status_code == 200
    assert client.patch(f"/v1/agents/{agent['id']}", headers=headers(), json={"model": "test"}).status_code == 200
    assert client.get("/v1/projects", headers=headers()).json()["items"]
    assert client.get("/v1/agents", headers=headers()).json()["items"]
    assert client.get("/v1/memories/search?q=SQLite", headers=headers()).json()["items"]
    assert client.post("/v1/memories/search", headers=headers(), json={"query": "SQLite", "limit": 5}).status_code == 200
    assert client.post("/v1/memories/batch", headers=headers(), json={"items": [{"title": "B", "content": "batch", "type": "fact", "project_id": project["id"]}]}).status_code == 201
    assert client.patch(f"/v1/memories/{memory['id']}", headers=headers(), json={"title": "Updated"}).status_code == 200
    for path, payload in (("archive", {}), ("restore", {}), ("pin", {"pinned": True}), ("supersede", {"replacement_memory_id": memory["id"]})):
        assert client.post(f"/v1/memories/{memory['id']}/{path}", headers=headers(), json=payload).status_code == 200
    assert client.get(f"/v1/memories/{memory['id']}/revisions", headers=headers()).status_code == 200
    assert client.post(f"/v1/memories/{memory['id']}/links", headers=headers(), json={"target_memory_id": memory["id"], "relation": "related"}).status_code == 201
    assert client.post(f"/v1/memories/{memory['id']}/feedback", headers=headers(), json={"rating": "useful"}).status_code == 201
    assert client.get("/v1/projects?sort=unknown", headers=headers()).status_code == 400


def test_cursor_pagination_and_filters(client):
    project, agent, _ = seed(client)
    for index in range(3):
        assert client.post("/v1/memories", headers=headers(), json={"title": f"M{index}", "content": "cursor", "type": "fact", "project_id": project["id"], "importance": index + 1, "tags": ["cursor"]}).status_code == 201
    first = client.get("/v1/memories?project_id=%s&limit=2&tag=cursor" % project["id"], headers=headers()).json()
    assert len(first["items"]) == 2 and first["has_more"] and first["next_cursor"]
    second = client.get("/v1/memories?project_id=%s&limit=2&tag=cursor&cursor=%s" % (project["id"], first["next_cursor"]), headers=headers()).json()
    assert len(second["items"]) == 1 and not second["has_more"]


def test_tasks_priority_assignment_agent_progress_and_events(client):
    project, agent, _ = seed(client)
    created = client.post("/v1/tasks", headers=headers(), json={
        "project_id": project["id"], "title": "  Update route tests  ",
        "description": "<h2>Acceptance criteria</h2><ul><li>Pass tests</li></ul>",
        "priority": "high",
    })
    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Update route tests"
    assert task["description"].startswith("<h2>")
    assert task["priority"] == "high" and task["status"] == "open"

    claimed = client.post(f"/v1/tasks/{task['id']}/claim", headers=headers(), json={
        "agent_id": agent["id"], "note": "Starting the tests",
    })
    assert claimed.status_code == 200
    assert claimed.json()["status"] == "working"
    assert claimed.json()["agent_id"] == agent["id"]

    done = client.patch(f"/v1/tasks/{task['id']}", headers=headers(), json={
        "actor_agent_id": agent["id"], "status": "done", "note": "Verified",
    })
    assert done.status_code == 200
    assert done.json()["status"] == "done" and done.json()["completed_at"]
    assert client.get(f"/v1/tasks?project_id={project['id']}&status=done&priority=high", headers=headers()).json()["items"][0]["id"] == task["id"]
    events = client.get(f"/v1/tasks/{task['id']}/events", headers=headers()).json()["items"]
    assert [event["action"] for event in events] == ["created", "claimed", "status_changed"]
    assert events[-1]["from_status"] == "working" and events[-1]["to_status"] == "done"
    assert client.patch(f"/v1/tasks/{task['id']}", headers=headers(), json={"status": "unknown"}).status_code == 422
    assert client.post(f"/v1/tasks/{task['id']}/events", headers=headers(), json={"note": " "}).status_code == 422


def test_task_file_upload_persists_safe_server_path_and_source_path(client, tmp_path, monkeypatch):
    project, _, _ = seed(client)
    monkeypatch.setenv("MEMORY_ATTACHMENT_DIR", str(tmp_path / "attachments"))
    task = client.post("/v1/tasks", headers=headers(), json={
        "project_id": project["id"], "title": "Inspect module file",
        "description": "Review the attached source file.",
    }).json()
    response = client.post(
        f"/v1/tasks/{task['id']}/attachments", headers=headers(),
        data={"source_paths": "lib/example.dart"},
        files={"files": ("../../example.dart", b"void main() {}", "text/plain")},
    )
    assert response.status_code == 201
    attachment = response.json()["items"][0]
    assert attachment["source_path"] == "lib/example.dart"
    assert attachment["name"] == "example.dart"
    stored_path = Path(attachment["path"])
    assert stored_path.is_absolute() and stored_path.is_relative_to(tmp_path / "attachments")
    assert stored_path.read_bytes() == b"void main() {}"
    download = client.get(
        f"/v1/tasks/{task['id']}/attachments/{attachment['id']}/download",
        headers=headers(),
    )
    assert download.status_code == 200 and download.content == b"void main() {}"
    assert client.get(f"/v1/tasks/{task['id']}", headers=headers()).json()["attachments"][0]["path"] == str(stored_path)


def test_task_ui_has_rich_editor_and_drop_support(client):
    response = client.get("/ui")
    assert response.status_code == 200
    assert 'data-tab="tasks"' in response.text
    assert "quill@2.0.3" in response.text
    assert "task-drop" in response.text and "source_paths" in response.text
    assert all(format_name in response.text for format_name in ("blockquote", "code-block", "video", "indent"))


def test_task_schema_migrates_without_losing_existing_records(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_API_KEY", "dev-key")
    path = tmp_path / "legacy-memory.db"
    store = SQLiteStore(str(path))
    client = TestClient(create_app(store), client=("127.0.0.1", 1234))
    project, _, memory = seed(client)
    with store.db:
        store.db.execute("DROP TABLE task_events")
        store.db.execute("DROP TABLE task_attachments")
        store.db.execute("DROP TABLE tasks")
    store.db.close()

    migrated = SQLiteStore(str(path))
    assert migrated.get(UUID(project["id"]), Project)
    assert migrated.get(UUID(memory["id"]), Memory)
    migrated_client = TestClient(create_app(migrated), client=("127.0.0.1", 1234))
    task = migrated_client.post("/v1/tasks", headers=headers(), json={
        "project_id": project["id"], "title": "Survives restart",
    })
    assert task.status_code == 201
    migrated.db.close()
    reopened = SQLiteStore(str(path))
    assert reopened.task_get(UUID(task.json()["id"])).title == "Survives restart"
    assert reopened.get(UUID(memory["id"]), Memory)


def test_idempotency_conflict_and_instruction_lifecycle(client):
    project, agent, memory = seed(client)
    payload = {"title": "Idempotent", "content": "one", "type": "fact", "project_id": project["id"]}
    first = client.post("/v1/memories", headers={**headers(), "Idempotency-Key": "same"}, json=payload)
    second = client.post("/v1/memories", headers={**headers(), "Idempotency-Key": "same"}, json=payload)
    conflict = client.post("/v1/memories", headers={**headers(), "Idempotency-Key": "same"}, json={**payload, "content": "two"})
    assert first.status_code == second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
    assert conflict.status_code == 409
    instruction = client.post("/v1/instructions", headers=headers(), json={"title": "Policy", "content": "Do it", "scope": "project", "project_id": project["id"], "priority": 50, "source": "agent", "status": "pending"}).json()
    assert client.post(f"/v1/instructions/{instruction['id']}/approve", headers=headers(), json={}).status_code == 200
    assert client.post(f"/v1/instructions/{instruction['id']}/approve", headers={**headers(), "X-API-Key": "dev-key"}, json={}).status_code == 200
    assert client.patch(f"/v1/instructions/{instruction['id']}", headers=headers(), json={"priority": 80}).status_code == 200


def test_sessions_context_maintenance_portability_and_admin(client, tmp_path):
    project, agent, memory = seed(client)
    session = client.post("/v1/sessions", headers=headers(), json={"project_id": project["id"], "agent_id": agent["id"], "task": "test"}).json()
    sid = session["id"]
    event = {"role": "assistant", "kind": "message", "content": "hello"}
    assert client.post(f"/v1/sessions/{sid}/events", headers={**headers(), "Idempotency-Key": "event-1"}, json=event).status_code == 201
    assert client.post(f"/v1/sessions/{sid}/events/batch", headers=headers(), json={"events": [event]}).status_code == 201
    assert client.get(f"/v1/sessions/{sid}/events", headers=headers()).status_code == 200
    assert client.put(f"/v1/sessions/{sid}/summary", headers=headers(), json={"summary": "done"}).status_code == 200
    assert client.get(f"/v1/sessions/{sid}/summary", headers=headers()).status_code == 200
    assert client.post("/v1/context", headers=headers(), json={"project_id": project["id"], "agent_id": agent["id"], "task": "find", "max_tokens": 1000, "limit_memories": 5}).status_code == 200
    assert client.post("/v1/context/preview", headers=headers(), json={"project_id": project["id"], "agent_id": agent["id"], "task": "find", "max_tokens": 1000, "limit_memories": 5}).status_code == 200
    assert client.post("/v1/context/feedback", headers=headers(), json={"project_id": project["id"], "agent_id": agent["id"], "outcome": "success"}).status_code == 201
    assert client.post("/v1/maintenance/deduplicate", headers=headers(), json={"project_id": project["id"]}).status_code == 200
    export = client.post("/v1/export", headers=headers(), json={"project_id": project["id"]})
    assert export.status_code == 200 and "attachment" in export.headers["content-disposition"]
    data = "\n".join([json.dumps({"record_type": "memory", "title": "Imported", "content": "x", "type": "fact", "project_id": project["id"]})])
    assert client.post("/v1/import", headers=headers(), files={"file": ("import.jsonl", io.BytesIO(data.encode()), "application/jsonl")}, data={"project_id": project["id"], "dry_run": "true"}).status_code == 200
    assert client.get("/v1/admin/backups", headers={"X-API-Key": "dev-key"}).status_code == 200
    assert client.post("/v1/admin/backup", headers={"X-API-Key": "dev-key"}, json={"destination": "test.sqlite"}).status_code == 200


def test_openapi_contains_every_spec_path(client):
    actual = set(client.get("/openapi.json").json()["paths"])
    required = {
        "/health", "/v1/meta", "/v1/stats", "/v1/projects", "/v1/projects/{project_id}",
        "/v1/agents", "/v1/agents/{agent_id}", "/v1/instructions", "/v1/instructions/{instruction_id}",
        "/v1/tasks", "/v1/tasks/{task_id}", "/v1/tasks/{task_id}/claim",
        "/v1/tasks/{task_id}/events", "/v1/tasks/{task_id}/attachments",
        "/v1/tasks/{task_id}/attachments/{attachment_id}/download",
        "/v1/instructions/{instruction_id}/approve", "/v1/instructions/{instruction_id}/revoke",
        "/v1/memories", "/v1/memories/batch", "/v1/memories/search", "/v1/memories/{memory_id}",
        "/v1/memories/{memory_id}/archive", "/v1/memories/{memory_id}/restore", "/v1/memories/{memory_id}/pin",
        "/v1/memories/{memory_id}/supersede", "/v1/memories/{memory_id}/revisions", "/v1/memories/{memory_id}/links",
        "/v1/memories/{memory_id}/links/{link_id}", "/v1/memories/{memory_id}/feedback", "/v1/sessions",
        "/v1/sessions/{session_id}", "/v1/sessions/{session_id}/close", "/v1/sessions/{session_id}/events",
        "/v1/sessions/{session_id}/events/batch", "/v1/sessions/{session_id}/summary", "/v1/events/search",
        "/v1/context", "/v1/context/preview", "/v1/context/feedback", "/v1/audit", "/v1/maintenance/expire",
        "/v1/maintenance/deduplicate", "/v1/export", "/v1/import", "/v1/admin/backup", "/v1/admin/backups",
    }
    assert required <= actual


def test_member_task_isolation_and_approval(client):
    project, agent, _ = seed(client)
    first = client.post('/v1/members', headers=headers(), json={'name': 'First', 'api_key': 'first-member-key-001'}).json()
    second = client.post('/v1/members', headers=headers(), json={'name': 'Second', 'api_key': 'second-member-key-002'}).json()
    one, two = headers(first['api_key']), headers(second['api_key'])
    assert client.get('/v1/me', headers=one).json()['allowed_tabs'] == ['tasks', 'projects']
    assert 'members' in client.get('/v1/me', headers=headers()).json()['allowed_tabs']
    task = client.post('/v1/tasks', headers=one, json={'project_id': project['id'], 'title': 'Private submission'}).json()
    path = '/v1/tasks/' + task['id']
    assert not task['approved']
    assert client.get('/v1/tasks', headers=one).json()['items'][0]['id'] == task['id']
    assert client.get('/v1/tasks', headers=two).json()['items'] == []
    assert client.get(path, headers=two).status_code == 404
    assert client.get(path, headers=one).status_code == 200
    assert client.get('/v1/members', headers=one).status_code == 403
    assert client.post(path+'/approve', headers=one).status_code == 403
    assert client.post(path+'/claim', headers=headers(), json={'agent_id': agent['id']}).status_code == 409
    assert client.post(path+'/approve', headers=headers()).status_code == 200
    assert client.patch(path, headers=headers(), json={'status':'working'}).status_code == 200
    assert client.get(path, headers=one).json()['status'] == 'working'
    assert client.get('/v1/tasks', headers=headers('test-key')).json()['items'] == []
    assert 'key_hash' not in str(client.get('/v1/members', headers=headers()).json())


def test_task_close_delete_permissions(client):
    project, _, _ = seed(client)
    tester = headers('test-key')
    task = client.post('/v1/tasks', headers=tester, json={'project_id': project['id'], 'title': 'Close and delete'}).json()
    path = '/v1/tasks/' + task['id']
    assert client.patch(path, headers=tester, json={'status': 'closed'}).status_code == 200
    assert client.patch(path, headers=headers(), json={'status': 'closed'}).json()['status'] == 'closed'
    assert client.get(path, headers=tester).json()['status'] == 'closed'
    assert client.delete(path, headers=headers()).json()['deleted'] is True
    assert client.get(path, headers=headers()).status_code == 404
    assert client.get(path+'/events', headers=headers()).status_code == 404


def test_member_status_changes_and_creator_filter(client):
    project, _, _ = seed(client)
    member = client.post('/v1/members', headers=headers(), json={'name': 'Creator', 'api_key': 'creator-member-key-003'}).json()
    own = headers(member['api_key'])
    task = client.post('/v1/tasks', headers=own, json={'project_id': project['id'], 'title': 'Own task'}).json()
    other = client.post('/v1/tasks', headers=headers('test-key'), json={'project_id': project['id'], 'title': 'Other task'}).json()
    path = '/v1/tasks/' + task['id']
    for status in ['closed', 'reopened', 'open']:
        response = client.patch(path, headers=own, json={'status': status})
        assert response.status_code == 200
        assert response.json()['status'] == status
        assert not response.json()['approved']
    for body in [{'status':'working'}, {'status':'done'}, {'status':'open','agent_id':None}]:
        assert client.patch(path, headers=own, json=body).status_code == 403
    assert client.patch(path, headers=own, json={'status':'open','approved':True}).status_code == 422
    assert client.patch('/v1/tasks/'+other['id'], headers=own, json={'status':'closed'}).status_code == 404
    assert client.delete('/v1/tasks/'+other['id'], headers=own).status_code == 404
    filtered = client.get('/v1/tasks?creator_id='+member['id'], headers=headers()).json()['items']
    assert [t['id'] for t in filtered] == [task['id']]
    filtered = client.get('/v1/tasks?creator_id=builtin-test', headers=own).json()['items']
    assert [t['id'] for t in filtered] == [task['id']]


def test_member_can_edit_and_delete_own_task(client):
    project, agent, _ = seed(client)
    owner = headers('test-key')
    task = client.post('/v1/tasks', headers=owner, json={'project_id': project['id'], 'title':'Original'}).json()
    path = '/v1/tasks/'+task['id']
    client.post(path+'/approve', headers=headers())
    client.post(path+'/claim', headers=headers(), json={'agent_id':agent['id']})
    changed = client.patch(path, headers=owner, json={'title':'Updated', 'description':'New requirements', 'priority':'high'})
    assert changed.status_code == 200
    assert changed.json()['title'] == 'Updated'
    assert changed.json()['status'] == 'reopened'
    assert changed.json()['approved'] is False
    assert client.post(path+'/claim', headers=headers(), json={'agent_id':agent['id']}).status_code == 409
    assert client.patch(path, headers=owner, json={'title':' '}).status_code == 422
    assert client.patch(path, headers=owner, json={'actor_agent_id':agent['id']}).status_code == 403
    other = client.post('/v1/members', headers=headers(), json={'name':'Other', 'api_key': 'other-member-key-004'}).json()
    assert client.patch(path, headers=headers(other['api_key']), json={'title':'Hijack'}).status_code == 404
    assert client.delete(path, headers=headers(other['api_key'])).status_code == 404
    assert client.delete(path, headers=owner).json()['deleted'] is True
    assert client.get(path, headers=owner).status_code == 404

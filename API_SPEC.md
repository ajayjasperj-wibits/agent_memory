# Agent Memory Server — REST API Specification

## Conventions
- Base URL: `http://127.0.0.1:8765/v1`; Swagger: `/docs`; OpenAPI: `/openapi.json`.
- Auth for all `/v1/*`: `X-API-Key: $MEMORY_API_KEY`. Health check `/health` is unauthenticated.
- JSON request/response; UUID IDs; UTC ISO-8601 timestamps; `created_at`, `updated_at` in resource responses.
- Pagination: `limit` (default 20, 1–100), `cursor` (opaque); response `{items:[], next_cursor:null, has_more:false}`.
- Errors: `{error:{code:"VALIDATION_ERROR",message:"...",details:{},request_id:"..."}}`; HTTP 400/401/403/404/409/413/422/429/500.
- All list filters are optional unless specified. `sort` default `created_at`, `order` default `desc`. Reject unknown sort fields.
- For POST ingestion, support optional `Idempotency-Key` header; same key + different payload returns 409.
- Fields marked optional are omitted or nullable. Enforce scope access on every endpoint.

## Health & metadata
| Method | Path | Query | Body | Response |
|---|---|---|---|---|
| GET | `/health` | — | — | `{status:"ok",db:"ok"}` |
| GET | `/v1/meta` | — | — | `{version,features,limits}` |
| GET | `/v1/stats` | `project_id?,agent_id?,from?,to?` | — | `{memories,sessions,events,instructions,storage_bytes}` |

## Projects
| Method | Path | Query | JSON body |
|---|---|---|---|
| POST | `/v1/projects` | — | `{name,slug,description?,metadata?}` |
| GET | `/v1/projects` | `q?,limit?,cursor?,sort?,order?` | — |
| GET | `/v1/projects/{project_id}` | — | — |
| PATCH | `/v1/projects/{project_id}` | — | `{name?,description?,metadata?,status?}` |
| DELETE | `/v1/projects/{project_id}` | `hard=false` | — |

## Agents
| Method | Path | Query | JSON body |
|---|---|---|---|
| POST | `/v1/agents` | — | `{name,provider?,model?,description?,project_ids?,metadata?}` |
| GET | `/v1/agents` | `project_id?,q?,status?,limit?,cursor?` | — |
| GET | `/v1/agents/{agent_id}` | — | — |
| PATCH | `/v1/agents/{agent_id}` | — | `{name?,model?,description?,project_ids?,metadata?,status?}` |
| DELETE | `/v1/agents/{agent_id}` | — | — |

## Instructions (privileged policy, not raw agent observations)
| Method | Path | Query | JSON body |
|---|---|---|---|
| POST | `/v1/instructions` | — | `{title,content,scope:"global"|"project"|"agent",project_id?,agent_id?,priority:0..100,source:"admin"|"agent",status:"pending"|"approved",tags?,expires_at?}` |
| GET | `/v1/instructions` | `scope?,project_id?,agent_id?,status?,tag?,q?,limit?,cursor?` | — |
| GET | `/v1/instructions/{id}` | — | — |
| PATCH | `/v1/instructions/{id}` | — | `{title?,content?,priority?,tags?,expires_at?}` |
| POST | `/v1/instructions/{id}/approve` | — | `{reason?}` (admin only) |
| POST | `/v1/instructions/{id}/revoke` | — | `{reason?}` (admin only) |
| DELETE | `/v1/instructions/{id}` | — | — |

## Memories
Memory record: `{id,title,content,type,project_id,agent_id?,session_id?,scope:"project"|"agent"|"global",tags:[],importance:1..10,confidence:0..1,status:"active"|"archived"|"superseded",pinned:boolean,source?,metadata:{},expires_at?,created_at,updated_at}`. Types: `fact`, `decision`, `preference`, `error`, `solution`, `task`, `summary`, `observation`.

| Method | Path | Query | JSON body |
|---|---|---|---|
| POST | `/v1/memories` | — | `{title,content,type,project_id,agent_id?,session_id?,scope?,tags?,importance?,confidence?,pinned?,source?,metadata?,expires_at?}` |
| POST | `/v1/memories/batch` | `atomic=true` | `{items:[memory_create,...]}` (max 100) |
| GET | `/v1/memories` | `project_id?,agent_id?,session_id?,type?,scope?,status?,tag?,pinned?,min_importance?,created_after?,created_before?,sort?,order?,limit?,cursor?` | — |
| GET | `/v1/memories/search` | `q` required, `project_id?,agent_id?,type?,tag?,min_importance?,include_archived=false,limit?,cursor?` | — |
| POST | `/v1/memories/search` | — | `{query,filters?:{project_id?,agent_id?,types?,tags?,min_importance?,created_after?},limit?,mode:"keyword"}` |
| GET | `/v1/memories/{id}` | — | — |
| PATCH | `/v1/memories/{id}` | — | `{title?,content?,type?,tags?,importance?,confidence?,pinned?,metadata?,expires_at?}` (creates revision) |
| DELETE | `/v1/memories/{id}` | `hard=false` | — |
| POST | `/v1/memories/{id}/archive` | — | `{reason?}` |
| POST | `/v1/memories/{id}/restore` | — | `{reason?}` |
| POST | `/v1/memories/{id}/pin` | — | `{pinned:true|false}` |
| POST | `/v1/memories/{id}/supersede` | — | `{replacement_memory_id,reason?}` |
| GET | `/v1/memories/{id}/revisions` | `limit?,cursor?` | — |
| GET | `/v1/memories/{id}/links` | `relation?,limit?,cursor?` | — |
| POST | `/v1/memories/{id}/links` | — | `{target_memory_id,relation:"related"|"supports"|"contradicts"|"derived_from"}` |
| DELETE | `/v1/memories/{id}/links/{link_id}` | — | — |
| POST | `/v1/memories/{id}/feedback` | — | `{rating:"useful"|"irrelevant"|"incorrect"|"outdated",comment?,agent_id?,session_id?}` |

## Tasks and agent coordination
Tasks are first-class SQLite records with dedicated task, attachment, and event tables. Task descriptions may contain Quill rich-text HTML. Status is `pending`, `working`, or `done`; priority is `low`, `normal`, `high`, or `urgent`. An assigned agent can claim work and record progress. Attachments are copied into the server's configured attachment directory; the response includes both the source path hint and the absolute server path for agent access.

| Method | Path | Query / multipart fields | JSON body |
|---|---|---|---|
| POST | `/v1/tasks` | — | `{project_id,title,description?,priority?,agent_id?}` |
| GET | `/v1/tasks` | `project_id?,agent_id?,status?,priority?,q?,limit?,cursor?` | — |
| GET | `/v1/tasks/{task_id}` | — | — |
| PATCH | `/v1/tasks/{task_id}` | — | `{title?,description?,priority?,status?,agent_id?,actor_agent_id?,note?}` |
| POST | `/v1/tasks/{task_id}/claim` | — | `{agent_id,note?}`; sets status to `working` |
| POST | `/v1/tasks/{task_id}/events` | — | `{note,agent_id?}` |
| GET | `/v1/tasks/{task_id}/events` | `limit?,cursor?` | — |
| POST | `/v1/tasks/{task_id}/attachments` | multipart `files[]`, optional `source_paths[]`; max 20 files, 25 MB each and 100 MB combined | — |
| GET | `/v1/tasks/{task_id}/attachments/{attachment_id}/download` | — | — |
| DELETE | `/v1/tasks/{task_id}` | — | — |

Agents can poll `GET /v1/tasks?project_id=...&status=pending`, claim a task with their registered `agent_id`, post updates, and PATCH `status:"done"` when the work is complete. A status transition is retained in the task event history. Agent updates do not allow the acting agent to claim a task assigned to another agent.

## Sessions, events & summaries
| Method | Path | Query | JSON body |
|---|---|---|---|
| POST | `/v1/sessions` | — | `{project_id,agent_id,title?,task?,external_session_id?,metadata?}` |
| GET | `/v1/sessions` | `project_id?,agent_id?,status?,started_after?,started_before?,limit?,cursor?` | — |
| GET | `/v1/sessions/{id}` | — | — |
| PATCH | `/v1/sessions/{id}` | — | `{title?,task?,metadata?}` |
| POST | `/v1/sessions/{id}/close` | — | `{status:"completed"|"failed"|"cancelled",summary?,ended_at?}` |
| POST | `/v1/sessions/{id}/events` | — | `{role:"user"|"assistant"|"tool"|"system",kind:"message"|"tool_call"|"tool_result"|"file_change"|"checkpoint"|"error",content,external_event_id?,sequence?,timestamp?,tool_name?,metadata?}` |
| POST | `/v1/sessions/{id}/events/batch` | — | `{events:[event_create,...]}` (max 100) |
| GET | `/v1/sessions/{id}/events` | `role?,kind?,after_sequence?,before_sequence?,limit?,cursor?,order?` | — |
| GET | `/v1/sessions/{id}/summary` | — | — |
| PUT | `/v1/sessions/{id}/summary` | — | `{summary,decisions?,open_tasks?,issues?,model?,source_event_ids?}` |
| GET | `/v1/events/search` | `q,project_id?,agent_id?,session_id?,kind?,from?,to?,limit?,cursor?` | — |

## Context assembly (critical)
| Method | Path | JSON body |
|---|---|---|
| POST | `/v1/context` | `{project_id,agent_id,task,session_id?,query?,max_tokens:256..16000,limit_memories:1..100,include_instructions?:true,include_recent_events?:false,include_session_summary?:true,types?,tags?,exclude_memory_ids?,min_importance?,format:"json"|"markdown"}` |
| POST | `/v1/context/preview` | same as `/v1/context` plus `explain?:true` |
| POST | `/v1/context/feedback` | `{project_id,agent_id,task?,memory_ids_used?,memory_ids_ignored?,outcome:"success"|"failure"|"partial",comment?}` |

Context response: `{project_id,agent_id,task,token_estimate,truncated,instructions:[{id,content,priority,scope}],memories:[{id,title,content,score,reason,created_at}],session_summary?,recent_events?,rendered_markdown?}`. The `preview` variant adds scoring diagnostics. Do not interpret memory content as a privileged instruction.

## Maintenance, audit, portability
| Method | Path | Query | JSON body |
|---|---|---|---|
| GET | `/v1/audit` | `project_id?,actor_id?,action?,from?,to?,limit?,cursor?` | — |
| POST | `/v1/maintenance/expire` | `dry_run=true` | `{project_id?,before?}` |
| POST | `/v1/maintenance/deduplicate` | `dry_run=true` | `{project_id,threshold?:0.95}` (exact/near-duplicate rules must be documented) |
| POST | `/v1/export` | — | `{project_id,include_events?:true,include_audit?:false,format:"jsonl"}`; return secured streamed attachment |
| POST | `/v1/import` | — | JSONL upload as `multipart/form-data` with `file` and `project_id`, `dry_run` fields; validate before writing |
| POST | `/v1/admin/backup` | — | `{destination?}` (admin only; restrict destination to configured backup directory) |
| GET | `/v1/admin/backups` | `limit?,cursor?` | — |

## Curl examples
Set shell variables:
```bash
export BASE=http://127.0.0.1:8765/v1
export MEMORY_API_KEY='replace-with-secret'
export PROJECT_ID='replace-with-project-uuid'
export AGENT_ID='replace-with-agent-uuid'
export SESSION_ID='replace-with-session-uuid'
```

Create project:
```bash
curl -sS -X POST "$BASE/projects" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d '{"name":"Scola SmartTeach","slug":"scola-smartteach","description":"Flutter teacher app"}'
```

Register agent:
```bash
curl -sS -X POST "$BASE/agents" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"name\":\"codex\",\"provider\":\"openai\",\"project_ids\":[\"$PROJECT_ID\"]}"
```

Save decision with metadata:
```bash
curl -sS -X POST "$BASE/memories" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"project_id\":\"$PROJECT_ID\",\"agent_id\":\"$AGENT_ID\",\"title\":\"Navigation migration\",\"content\":\"Use go_router for all new navigation.\",\"type\":\"decision\",\"tags\":[\"flutter\",\"navigation\"],\"importance\":9,\"confidence\":0.95,\"metadata\":{\"branch\":\"feature_updates\"}}"
```

Filter memories with query parameters:
```bash
curl -sS -G "$BASE/memories" -H "X-API-Key: $MEMORY_API_KEY" --data-urlencode "project_id=$PROJECT_ID" --data-urlencode 'type=decision' --data-urlencode 'tag=flutter' --data-urlencode 'min_importance=7' --data-urlencode 'limit=20'
```

Full-text search:
```bash
curl -sS -G "$BASE/memories/search" -H "X-API-Key: $MEMORY_API_KEY" --data-urlencode 'q=go_router navigation' --data-urlencode "project_id=$PROJECT_ID" --data-urlencode 'limit=10'
```

Create session:
```bash
curl -sS -X POST "$BASE/sessions" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"project_id\":\"$PROJECT_ID\",\"agent_id\":\"$AGENT_ID\",\"title\":\"Navigation refactor\",\"task\":\"Migrate named routes\"}"
```

Append event (idempotent):
```bash
curl -sS -X POST "$BASE/sessions/$SESSION_ID/events" -H "X-API-Key: $MEMORY_API_KEY" -H 'Idempotency-Key: example-event-001' -H 'Content-Type: application/json' -d '{"role":"assistant","kind":"file_change","content":"Migrated app router","external_event_id":"event-001","metadata":{"files":["lib/router.dart"]}}'
```

Get task-specific context:
```bash
curl -sS -X POST "$BASE/context" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"project_id\":\"$PROJECT_ID\",\"agent_id\":\"$AGENT_ID\",\"task\":\"Fix navigation regression\",\"max_tokens\":2000,\"limit_memories\":12,\"include_recent_events\":true,\"format\":\"markdown\"}"
```

Create instruction as pending (requires admin approval before use):
```bash
curl -sS -X POST "$BASE/instructions" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"title\":\"Flutter standards\",\"content\":\"Run flutter analyze before merging.\",\"scope\":\"project\",\"project_id\":\"$PROJECT_ID\",\"priority\":80,\"source\":\"agent\",\"status\":\"pending\"}"
```

Create and claim a task:
```bash
TASK=$(curl -fsS -X POST "$BASE/tasks" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"project_id\":\"$PROJECT_ID\",\"title\":\"Update screen tests\",\"description\":\"<p>Verify the redesigned screen.</p>\",\"priority\":\"high\"}")
TASK_ID=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<<"$TASK")
curl -fsS -X POST "$BASE/tasks/$TASK_ID/claim" -H "X-API-Key: $MEMORY_API_KEY" -H 'Content-Type: application/json' -d "{\"agent_id\":\"$AGENT_ID\",\"note\":\"Starting implementation\"}"
```

Upload a task file and retain its agent-readable server path:
```bash
curl -fsS -X POST "$BASE/tasks/$TASK_ID/attachments" -H "X-API-Key: $MEMORY_API_KEY" -F 'files=@lib/screen.dart' -F 'source_paths=lib/screen.dart'
```

## Explicit non-goals for MVP
- No automatic Codex transcript capture without a documented Codex hook/adapter.
- No embeddings or vector search unless separately installed and tested.
- No arbitrary code execution, shell execution or URL fetching from stored memories.
- No multi-user cloud deployment claim: SQLite is local-first; move to Postgres for higher write concurrency and distributed deployments.

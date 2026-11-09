import os
import logging
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from agent_memory.application.services import AgentService, MemoryService, ProjectService
from agent_memory.domain.models import Agent, Memory, Project
from agent_memory.infrastructure.sqlite import SQLiteRepository, SQLiteStore
from agent_memory.interfaces.http import build_router
from agent_memory.ui import ui_response

logger = logging.getLogger(__name__)


def create_app(store=None) -> FastAPI:
    store = store or SQLiteStore(os.getenv("MEMORY_DB_PATH", "memory.db"))
    project_repository = SQLiteRepository(store, Project)
    agent_repository = SQLiteRepository(store, Agent)
    memory_repository = SQLiteRepository(store, Memory)
    projects = ProjectService(project_repository)
    agents = AgentService(agent_repository, projects)
    memories = MemoryService(memory_repository, projects, agents)
    app = FastAPI(title="Agent Memory Server", version="0.1.0")

    app.state.store = store

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.scope["request_id"] = request_id
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Unhandled API error request_id=%s path=%s", request_id, request.url.path)
            response = JSONResponse(status_code=500, content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error", "details": {}, "request_id": request_id}})
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        request_id = request.scope.get("request_id", request.headers.get("X-Request-ID", ""))
        return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "message": "Request validation failed", "details": exc.errors(), "request_id": request_id}})

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        request_id = request.scope.get("request_id", request.headers.get("X-Request-ID", ""))
        detail = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
        return JSONResponse(status_code=exc.status_code, content={"error": {"code": detail.get("code", "HTTP_ERROR"), "message": detail.get("message", str(exc.detail)), "details": detail.get("details", {}), "request_id": request_id}})
    app.include_router(build_router(store, projects, agents, memories))

    @app.get("/health")
    def health():
        return {"status": "ok", "db": "ok"}

    @app.get("/ui", include_in_schema=False)
    def ui():
        return ui_response()

    return app


app = create_app()


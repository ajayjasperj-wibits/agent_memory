from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Project:
    name: str
    slug: str
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    status: str = "active"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Agent:
    name: str
    provider: str | None = None
    model: str | None = None
    description: str | None = None
    project_ids: list[UUID] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    status: str = "active"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Memory:
    title: str
    content: str
    type: str
    project_id: UUID
    agent_id: UUID | None = None
    session_id: UUID | None = None
    scope: str = "project"
    tags: list[str] = field(default_factory=list)
    importance: int = 5
    confidence: float = 1.0
    status: str = "active"
    pinned: bool = False
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    expires_at: datetime | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Task:
    title: str
    description: str
    project_id: UUID
    priority: str = "normal"
    status: str = "open"
    approved: bool = True
    creator_id: str | None = None
    agent_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None


from uuid import UUID

from agent_memory.domain.models import Agent, Memory, Project, utc_now


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class ProjectService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, project: Project) -> Project:
        if self.repository.by_slug(project.slug):
            raise ConflictError("A project with this slug already exists")
        return self.repository.create(project)

    def get(self, project_id: UUID) -> Project:
        project = self.repository.get(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project


class AgentService:
    def __init__(self, repository, projects=None):
        self.repository, self.projects = repository, projects

    def create(self, agent: Agent) -> Agent:
        if self.projects:
            for project_id in agent.project_ids: self.projects.get(project_id)
        return self.repository.create(agent)

    def get(self, agent_id: UUID) -> Agent:
        agent = self.repository.get(agent_id)
        if not agent:
            raise NotFoundError("Agent not found")
        return agent


class MemoryService:
    def __init__(self, repository, projects, agents):
        self.repository, self.projects, self.agents = repository, projects, agents

    def create(self, memory: Memory) -> Memory:
        self.projects.get(memory.project_id)
        if memory.agent_id:
            self.agents.get(memory.agent_id)
        if memory.scope == "agent" and not memory.agent_id:
            raise ValueError("Agent-scoped memories require agent_id")
        return self.repository.create(memory)

    def get(self, memory_id: UUID) -> Memory:
        memory = self.repository.get(memory_id)
        if not memory:
            raise NotFoundError("Memory not found")
        return memory

    def archive(self, memory_id: UUID) -> Memory:
        memory = self.get(memory_id)
        memory.status, memory.updated_at = "archived", utc_now()
        return self.repository.update(memory)


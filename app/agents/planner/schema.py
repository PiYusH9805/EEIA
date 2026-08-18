from pydantic import BaseModel
from enum import Enum


class AgentType(str, Enum):
    DOCUMENTATION = "documentation"
    CODE = "code"
    GITHUB = "github"
    BUG = "bug"


class PlannerResponse(BaseModel):
    agent: AgentType
    reason: str
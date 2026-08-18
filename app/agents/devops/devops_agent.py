from app.services.repository_service import RepositoryService
from app.services.llm_service import LLMService

from app.agents.devops.prompt import (
    DEVOPS_AGENT_PROMPT
)


class DevOpsAgent:

    def __init__(self):

        self.repository = RepositoryService()

    def ask(self, question: str):

        context = self.repository.get_repository_context()

        messages = [

            {
                "role": "system",
                "content": DEVOPS_AGENT_PROMPT
            },

            {
                "role": "user",
                "content": f"""
Repository Context:

{context}

DevOps Question:

{question}
"""
            }

        ]

        return LLMService.chat(
            messages=messages
        )
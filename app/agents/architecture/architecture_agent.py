from app.services.repository_service import RepositoryService
from app.services.llm_service import LLMService

from app.agents.architecture.prompt import (
    ARCHITECTURE_AGENT_PROMPT
)


class ArchitectureAgent:

    def __init__(self):

        self.repository = RepositoryService()

    def ask(self, question: str):

        context = self.repository.get_repository_context()

        messages = [

            {
                "role": "system",
                "content": ARCHITECTURE_AGENT_PROMPT
            },

            {
                "role": "user",
                "content": f"""
Repository Context:

{context}

Question:

{question}
"""
            }

        ]

        return LLMService.chat(
            messages=messages
        )
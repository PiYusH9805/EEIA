from app.services.repository_service import RepositoryService
from app.services.llm_service import LLMService

from app.agents.security.prompt import (
    SECURITY_AGENT_PROMPT
)


class SecurityAgent:

    def __init__(self):

        self.repository = RepositoryService()

    def ask(self, question: str):

        context = self.repository.get_repository_context()

        messages = [

            {
                "role": "system",
                "content": SECURITY_AGENT_PROMPT
            },

            {
                "role": "user",
                "content": f"""
Repository Context:

{context}

Security Question:

{question}
"""
            }

        ]

        return LLMService.chat(
            messages=messages
        )
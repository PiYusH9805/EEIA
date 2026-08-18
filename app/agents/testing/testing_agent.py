from app.services.repository_service import RepositoryService
from app.services.llm_service import LLMService

from app.agents.testing.prompt import (
    TESTING_AGENT_PROMPT
)


class TestingAgent:

    def __init__(self):

        self.repository = RepositoryService()

    def ask(self, question: str):

        context = self.repository.get_repository_context()

        messages = [

            {
                "role": "system",
                "content": TESTING_AGENT_PROMPT
            },

            {
                "role": "user",
                "content": f"""
Repository Context:

{context}

Testing Request:

{question}
"""
            }

        ]

        return LLMService.chat(
            messages=messages
        )
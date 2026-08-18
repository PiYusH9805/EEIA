from app.services.repository_service import RepositoryService
from app.services.llm_service import LLMService

from app.agents.review.prompt import (
    CODE_REVIEW_AGENT_PROMPT
)


class CodeReviewAgent:

    def __init__(self):
        print("[ReviewAgent] Initializing...")
        self.repository = RepositoryService()

    def ask(self, question: str):

        print("[ReviewAgent] Started")
        print("[ReviewAgent] Getting repository context...")

        context = self.repository.get_repository_context()

        print("[ReviewAgent] Repository context received")
        print("[ReviewAgent] Context length:", len(context))

        messages = [
            {
                "role": "system",
                "content": CODE_REVIEW_AGENT_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Repository Context:

{context}

Review Request:

{question}
"""
            }
        ]

        print("[ReviewAgent] Calling Azure LLM...")

        answer = LLMService.chat(
            messages=messages
        )

        print("[ReviewAgent] LLM response received")

        return answer
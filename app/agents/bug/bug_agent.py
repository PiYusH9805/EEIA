from app.services.llm_service import LLMService
from app.agents.bug.prompt import BUG_AGENT_PROMPT


class BugAgent:

    def ask(self, question: str):

        messages = [
            {
                "role": "system",
                "content": BUG_AGENT_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]

        answer = LLMService.chat(messages)

        return answer
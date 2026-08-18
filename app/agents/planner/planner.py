import json

from app.services.llm_service import LLMService
from app.services.planner_service import PlannerService
from app.router.router import AgentRouter
from app.agents.planner.prompt import PLANNER_SYSTEM_PROMPT


class PlannerAgent:

    def __init__(self):
        self.router = AgentRouter()

    def route(self, question: str):

        # -----------------------------
        # Rule Based Routing
        # -----------------------------
        detected_agent = PlannerService.detect_agent(question)

        if detected_agent:
            print(f"[PlannerService] Routed to: {detected_agent}")
            return self.router.execute(
                detected_agent,
                question
            )

        # -----------------------------
        # LLM Planner
        # -----------------------------
        messages = [
            {
                "role": "system",
                "content": PLANNER_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]

        result = LLMService.chat(messages)

        decision = json.loads(result)

        print(f"[PlannerLLM] Routed to: {decision['agent']}")

        return self.router.execute(
            decision["agent"],
            question
        )
import json
from app.services.llm_service import LLMService
from app.services.planner_service import PlannerService
from app.router.router import AgentRouter


class PlannerAgent:
    def __init__(self):
        self.router = AgentRouter()

    def plan(self, question, history=None, document_mode=False):
        if document_mode:
            return ['documentation']
        detected = PlannerService.detect_agents(question)
        if detected:
            # Inspect source before analysis; documentation comes after findings.
            order = ['code', 'architecture', 'github', 'bug', 'security', 'review', 'testing', 'devops', 'research', 'documentation']
            return [name for name in order if name in detected][:5]
        if question.lower().strip(' !.?') in ('hi', 'hello', 'hey', 'namaste', 'thanks', 'thank you'):
            return ['general']
        messages = [{'role': 'system', 'content':
            'Route the user request. Return a JSON object with an agents array containing 1 to 5 names from: '
            + ', '.join(self.router.names) + '. Use general for ordinary conversation. Use recent conversation to resolve follow-ups.'}]
        messages.extend((history or [])[-6:])
        messages.append({'role': 'user', 'content': question})
        raw = LLMService.chat(messages, response_format={'type': 'json_object'})
        try:
            decision = json.loads(raw.strip().removeprefix('```json').removesuffix('```').strip())
            names = decision.get('agents', [decision.get('agent')])
            if not isinstance(names, list) or not names or len(names) > 5 or any(name not in self.router.names for name in names):
                raise ValueError('Invalid agent plan')
            return list(dict.fromkeys(names))
        except (ValueError, TypeError, AttributeError):
            return ['general']

    def route(self, question):
        results = [self.router.execute(agent, question) for agent in self.plan(question)]
        return '\n\n'.join(results)

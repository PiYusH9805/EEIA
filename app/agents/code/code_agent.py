from app.services.repository_service import RepositoryService
from app.services.llm_service import LLMService
from app.agents.code.prompt import CODE_AGENT_SYSTEM_PROMPT


class CodeAgent:
    def __init__(self):
        self.repository = RepositoryService()

    def ask(self, question):
        context = '' if 'Repository source evidence:' in question else self.repository.get_source_context(question)
        return LLMService.chat([
            {'role': 'system', 'content': CODE_AGENT_SYSTEM_PROMPT},
            {'role': 'user', 'content': question + '\n\nSource evidence:\n' + context}])

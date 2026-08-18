from app.agents.documentation.documentation_agent import DocumentationAgent
from app.agents.code.code_agent import CodeAgent
from app.agents.bug.bug_agent import BugAgent
from app.agents.github.github_agent import GitHubAgent

from app.agents.architecture.architecture_agent import ArchitectureAgent
from app.agents.security.security_agent import SecurityAgent
from app.agents.review.review_agent import CodeReviewAgent
from app.agents.devops.devops_agent import DevOpsAgent
from app.agents.testing.testing_agent import TestingAgent


class AgentRouter:

    def __init__(self):

        self.documentation = DocumentationAgent()

        self.code = CodeAgent()

        self.bug = BugAgent()

        self.github = GitHubAgent()

        self.architecture = ArchitectureAgent()

        self.security = SecurityAgent()

        self.review = CodeReviewAgent()

        self.devops = DevOpsAgent()

        self.testing = TestingAgent()

    def execute(self, agent: str, question: str):

        if agent == "documentation":

            return self.documentation.ask(question)

        elif agent == "code":

            return self.code.ask(question)

        elif agent == "bug":

            return self.bug.ask(question)

        elif agent == "github":

            return self.github.ask(question)

        elif agent == "architecture":

            return self.architecture.ask(question)

        elif agent == "security":

            return self.security.ask(question)

        elif agent == "review":

            return self.review.ask(question)

        elif agent == "devops":

            return self.devops.ask(question)

        elif agent == "testing":

            return self.testing.ask(question)

        return f"Unknown agent: {agent}"
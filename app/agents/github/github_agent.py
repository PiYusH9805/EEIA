from pathlib import Path
from app.services.github_service import GitHubService
from app.services.llm_service import LLMService

from app.agents.github.prompt import (
    GITHUB_AGENT_PROMPT
)


class GitHubAgent:

    def __init__(self):

        self.github = GitHubService(str(Path(__file__).resolve().parents[3]))

    def ask(self, question: str):

        request = question.split("\n\nRecent conversation", 1)[0].removeprefix("User request:\n")
        q = request.lower()

        # ==========================================
        # STATUS
        # ==========================================

        if "status" in q:

            context = self.github.get_status()

        # ==========================================
        # BRANCH
        # ==========================================

        elif "branch" in q:

            context = f"""
Current Branch:

{self.github.get_current_branch()}

All Branches:

{self.github.get_branches()}
"""

        # ==========================================
        # COMMIT
        # ==========================================

        elif "commit" in q:

            context = self.github.get_recent_commits()

        # ==========================================
        # DIFF
        # ==========================================

        elif "diff" in q or "changed" in q:

            context = f"""
Git Diff:

{self.github.get_diff()}

Changed Files:

{self.github.get_changed_files()}
"""

        # ==========================================
        # FILE HISTORY
        # ==========================================

        elif "history" in q:

            filename = self._extract_filename(request)

            if filename:

                context = self.github.get_file_history(
                    filename
                )

            else:

                context = (
                    "Please specify a file name, "
                    "for example: planner.py"
                )

        # ==========================================
        # BLAME
        # ==========================================

        elif "blame" in q or "who modified" in q:

            filename = self._extract_filename(request)

            if filename:

                context = self.github.get_blame(
                    filename
                )

            else:

                context = (
                    "Please specify a file name."
                )

        # ==========================================
        # STATISTICS
        # ==========================================

        elif (
            "statistics" in q
            or "stats" in q
            or "analyze repository" in q
            or "repository analysis" in q
        ):

            context = self.github.get_repository_context()

        # ==========================================
        # DEFAULT
        # ==========================================

        else:

            context = self.github.get_repository_context()

        # ==========================================
        # LLM
        # ==========================================

        messages = [

            {
                "role": "system",
                "content": GITHUB_AGENT_PROMPT
            },

            {
                "role": "user",
                "content": f"""
Git Repository Data:

{context}

User Question:

{question}
"""
            }

        ]

        return LLMService.chat(
            messages=messages
        )

    # ==========================================
    # FILE NAME EXTRACTION
    # ==========================================

    @staticmethod
    def _extract_filename(question):

        words = question.split()

        for word in words:

            cleaned = word.strip(
                "\"'.,!?()[]{}"
            )

            if (
                cleaned.endswith(".py")
                or cleaned.endswith(".js")
                or cleaned.endswith(".java")
                or cleaned.endswith(".cpp")
                or cleaned.endswith(".ts")
            ):

                return cleaned

        return None
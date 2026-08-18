class PlannerService:

    @staticmethod
    def detect_agent(question: str):

        q = question.lower()

        # ==========================================
        # GITHUB
        # ==========================================

        github_keywords = [
            "git",
            "github",
            "commit",
            "commits",
            "branch",
            "branches",
            "status",
            "diff",
            "blame",
            "history",
            "contributor",
            "contributors",
            "pull request",
            "merge",
            "changelog",
            "release notes"
        ]

        # ==========================================
        # BUG
        # ==========================================

        bug_keywords = [
            "error",
            "bug",
            "exception",
            "traceback",
            "stack trace",
            "debug",
            "debugging",
            "crash",
            "failed",
            "failure",
            "syntax error",
            "module not found"
        ]

        # ==========================================
        # SECURITY
        # ==========================================

        security_keywords = [
            "security",
            "vulnerability",
            "vulnerabilities",
            "secret",
            "secrets",
            "api key",
            "apikey",
            "password",
            "token",
            "sql injection",
            "xss",
            "csrf",
            "authentication security",
            "authorization security",
            "prompt injection"
        ]

        # ==========================================
        # ARCHITECTURE
        # ==========================================

        architecture_keywords = [
            "architecture",
            "system design",
            "high level design",
            "architecture diagram",
            "component architecture",
            "data flow",
            "request flow",
            "system flow"
        ]

        # ==========================================
        # CODE REVIEW
        # ==========================================

        review_keywords = [
            "code review",
            "review code",
            "review this code",
            "code quality",
            "quality issues",
            "bad practices",
            "code smells",
            "maintainability"
        ]

        # ==========================================
        # DEVOPS
        # ==========================================

        devops_keywords = [
            "devops",
            "deployment",
            "deploy",
            "docker",
            "dockerfile",
            "docker compose",
            "ci/cd",
            "github actions",
            "pipeline",
            "production",
            "kubernetes",
            "monitoring"
        ]

        # ==========================================
        # TESTING
        # ==========================================

        testing_keywords = [
            "test",
            "tests",
            "testing",
            "unit test",
            "unit tests",
            "integration test",
            "pytest",
            "test cases",
            "generate tests",
            "test coverage"
        ]

        # ==========================================
        # DOCUMENTATION
        # ==========================================

        documentation_keywords = [
            "pdf",
            "document",
            "uploaded document",
            "uploaded pdf",
            "summarize document",
            "summarize pdf",
            "chapter",
            "notes"
        ]

        # ==========================================
        # CODE
        # ==========================================

        code_keywords = [
            ".py",
            ".js",
            ".java",
            ".cpp",
            ".ts",
            "source code",
            "function",
            "class",
            "method",
            "variable",
            "explain code",
            "explain file",
            "explain project",
            "project structure",
            "repository structure",
            "folder structure"
        ]

        # ==========================================
        # PRIORITY
        # ==========================================

        if any(word in q for word in github_keywords):
            return "github"

        if any(word in q for word in bug_keywords):
            return "bug"

        if any(word in q for word in security_keywords):
            return "security"

        if any(word in q for word in architecture_keywords):
            return "architecture"

        if any(word in q for word in review_keywords):
            return "review"

        if any(word in q for word in devops_keywords):
            return "devops"

        if any(word in q for word in testing_keywords):
            return "testing"

        if any(word in q for word in documentation_keywords):
            return "documentation"

        if any(word in q for word in code_keywords):
            return "code"

        return None
import subprocess
from pathlib import Path


class GitHubService:

    def __init__(self, root="."):
        self.root = Path(root)

    # ==========================================
    # RUN GIT COMMAND
    # ==========================================

    def run(self, command):

        try:
            result = subprocess.run(
                command,
                cwd=self.root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            if result.returncode != 0:
                return f"Git Error: {result.stderr.strip()}"

            return result.stdout.strip()

        except Exception as e:
            return f"Git Error: {str(e)}"

    # ==========================================
    # CURRENT BRANCH
    # ==========================================

    def get_current_branch(self):

        return self.run([
            "git",
            "branch",
            "--show-current"
        ])

    # ==========================================
    # ALL BRANCHES
    # ==========================================

    def get_branches(self):

        return self.run([
            "git",
            "branch"
        ])

    # ==========================================
    # GIT STATUS
    # ==========================================

    def get_status(self):

        return self.run([
            "git",
            "status",
            "--short",
            "--branch"
        ])

    # ==========================================
    # RECENT COMMITS
    # ==========================================

    def get_recent_commits(self, limit=10):

        return self.run([
            "git",
            "log",
            f"-{limit}",
            "--pretty=format:%h | %an | %ad | %s",
            "--date=short"
        ])

    # ==========================================
    # GIT DIFF
    # ==========================================

    def get_diff(self):

        return self.run([
            "git",
            "diff"
        ])

    # ==========================================
    # FILE HISTORY
    # ==========================================

    def get_file_history(self, filename, limit=20):

        return self.run([
            "git",
            "log",
            f"-{limit}",
            "--follow",
            "--pretty=format:%h | %an | %ad | %s",
            "--date=short",
            "--",
            filename
        ])

    # ==========================================
    # GIT BLAME
    # ==========================================

    def get_blame(self, filename):

        return self.run([
            "git",
            "blame",
            filename
        ])

    # ==========================================
    # CHANGED FILES
    # ==========================================

    def get_changed_files(self):

        return self.run([
            "git",
            "diff",
            "--name-status"
        ])

    # ==========================================
    # COMMIT STATISTICS
    # ==========================================

    def get_commit_statistics(self):

        return self.run([
            "git",
            "shortlog",
            "-s",
            "-n",
            "--all"
        ])

    # ==========================================
    # REPOSITORY STATISTICS
    # ==========================================

    def get_statistics(self):

        commits = self.get_recent_commits(20)

        branches = self.get_branches()

        status = self.get_status()

        changed_files = self.get_changed_files()

        contributors = self.get_commit_statistics()

        return {
            "current_branch": self.get_current_branch(),
            "branches": branches,
            "status": status,
            "commits": commits,
            "changed_files": changed_files,
            "contributors": contributors
        }

    # ==========================================
    # COMPLETE REPOSITORY CONTEXT
    # ==========================================

    def get_repository_context(self):

        statistics = self.get_statistics()

        return f"""
CURRENT BRANCH
{statistics['current_branch']}

BRANCHES
{statistics['branches']}

STATUS
{statistics['status']}

RECENT COMMITS
{statistics['commits']}

CHANGED FILES
{statistics['changed_files']}

CONTRIBUTORS
{statistics['contributors']}
"""
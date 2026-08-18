from pathlib import Path


class RepositoryParser:

    def __init__(self, root_path):
        self.root = Path(root_path)

        self.ignore = {
            "myenv",
            ".git",
            "__pycache__",
            ".idea",
            ".vscode",
            "node_modules",
            "chroma_db",
            ".streamlit"
        }

    def get_project_structure(self):

        structure = []

        for path in self.root.rglob("*"):

            relative = path.relative_to(self.root)

            # Ignore unwanted folders
            if any(part in self.ignore for part in relative.parts):
                continue

            structure.append(str(relative))

        return structure
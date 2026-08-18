import ast
from pathlib import Path


class DependencyParser:

    def __init__(self, root_path):

        self.root = Path(root_path)

        self.ignore = {
            "myenv",
            ".git",
            "__pycache__",
            ".idea",
            ".vscode",
            "node_modules",
            "chroma_db"
        }

    def parse(self):

        dependencies = []

        for file in self.root.rglob("*.py"):

            relative = file.relative_to(self.root)

            if any(part in self.ignore for part in relative.parts):
                continue

            try:

                source = file.read_text(
                    encoding="utf-8"
                )

                tree = ast.parse(source)

            except Exception:
                continue

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:
                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:
                        imports.append(node.module)

            dependencies.append(
                {
                    "file": str(relative),
                    "imports": imports
                }
            )

        return dependencies
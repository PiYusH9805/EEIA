import ast
from pathlib import Path
from app.tools.file_search import source_files


class CodeParser:

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

        project = []

        for file in source_files(self.root):
            if file.suffix != ".py":
                continue

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

            classes = []
            functions = []
            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    classes.append(
                        {
                            "name": node.name,
                            "line": node.lineno
                        }
                    )

                elif isinstance(node, ast.FunctionDef):

                    functions.append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "args": [
                                arg.arg
                                for arg in node.args.args
                            ]
                        }
                    )

                elif isinstance(node, ast.Import):

                    for alias in node.names:

                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imports.append(node.module)

            project.append(
                {
                    "file": str(relative),
                    "classes": classes,
                    "functions": functions,
                    "imports": imports,
                    "lines": len(source.splitlines())
                }
            )

        return project
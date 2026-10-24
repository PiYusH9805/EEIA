from app.tools.file_search import EXCLUDED
import os
import ast


class DependencyService:

    def __init__(self, root="."):

        self.root = root

    def analyze(self):

        dependencies = {}

        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in EXCLUDED and not os.path.islink(os.path.join(root, d))]

            for file in files:

                if not file.endswith(".py"):
                    continue

                path = os.path.join(root, file)

                try:

                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        tree = ast.parse(f.read())

                    imports = []

                    for node in ast.walk(tree):

                        if isinstance(node, ast.Import):

                            for alias in node.names:

                                imports.append(alias.name)

                        elif isinstance(node, ast.ImportFrom):

                            if node.module:

                                imports.append(node.module)

                    dependencies[path] = imports

                except Exception:

                    continue

        return dependencies
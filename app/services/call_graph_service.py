from app.tools.file_search import EXCLUDED
import ast
import os


class CallGraphService:

    def __init__(self, root="."):

        self.root = root

    def analyze(self):

        graph = {}

        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in EXCLUDED and not os.path.islink(os.path.join(root, d))]

            for file in files:

                if not file.endswith(".py"):
                    continue

                path = os.path.join(root, file)

                try:

                    with open(path, "r", encoding="utf-8") as f:

                        tree = ast.parse(f.read())

                except Exception:

                    continue

                for node in ast.walk(tree):

                    if isinstance(node, ast.FunctionDef):

                        calls = []

                        for child in ast.walk(node):

                            if isinstance(child, ast.Call):

                                if isinstance(child.func, ast.Name):

                                    calls.append(child.func.id)

                                elif isinstance(child.func, ast.Attribute):

                                    calls.append(child.func.attr)

                        graph[node.name] = calls

        return graph
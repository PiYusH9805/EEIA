import ast
from pathlib import Path


class SymbolSearch:

    def __init__(self, root="."):

        self.root = Path(root)

    def find_symbol(self, symbol):

        for file in self.root.rglob("*.py"):

            try:

                tree = ast.parse(file.read_text(encoding="utf-8"))

                for node in ast.walk(tree):

                    if isinstance(node, ast.ClassDef):

                        if node.name == symbol:

                            return {

                                "type": "class",

                                "file": str(file),

                                "line": node.lineno

                            }

                    elif isinstance(node, ast.FunctionDef):

                        if node.name == symbol.replace("()", ""):

                            return {

                                "type": "function",

                                "file": str(file),

                                "line": node.lineno

                            }

            except Exception:

                continue

        return None
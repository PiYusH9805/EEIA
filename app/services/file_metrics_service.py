import ast


class FileMetricsService:

    @staticmethod
    def analyze(code: str):

        tree = ast.parse(code)

        functions = 0
        classes = 0
        imports = 0

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                functions += 1

            elif isinstance(node, ast.ClassDef):
                classes += 1

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports += 1

        return {

            "lines": len(code.splitlines()),

            "functions": functions,

            "classes": classes,

            "imports": imports

        }
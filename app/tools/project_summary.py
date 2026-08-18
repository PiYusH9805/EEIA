from app.tools.repo_parser import RepositoryParser
from app.tools.code_parser import CodeParser
from app.tools.dependency_parser import DependencyParser


class ProjectSummary:

    def __init__(self, root_path="."):

        self.repo = RepositoryParser(root_path)
        self.code = CodeParser(root_path)
        self.dependency = DependencyParser(root_path)

    def generate(self):

        structure = self.repo.get_project_structure()
        code = self.code.parse()
        dependencies = self.dependency.parse()

        python_files = len(code)

        agents = 0
        services = 0
        tools = 0

        classes = 0
        functions = 0
        imports = 0

        for item in code:

            if "/agents/" in item["file"].replace("\\", "/"):
                agents += 1

            if "/services/" in item["file"].replace("\\", "/"):
                services += 1

            if "/tools/" in item["file"].replace("\\", "/"):
                tools += 1

            classes += len(item["classes"])
            functions += len(item["functions"])

        for item in dependencies:
            imports += len(item["imports"])

        return {
            "total_files": len(structure),
            "python_files": python_files,
            "agents": agents,
            "services": services,
            "tools": tools,
            "classes": classes,
            "functions": functions,
            "imports": imports
        }
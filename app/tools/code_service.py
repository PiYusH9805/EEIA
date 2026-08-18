from app.tools.repo_parser import RepositoryParser
from app.tools.code_parser import CodeParser
from app.tools.dependency_parser import DependencyParser
from app.tools.project_summary import ProjectSummary


class CodeService:

    def __init__(self, root_path="."):

        self.repo_parser = RepositoryParser(root_path)
        self.code_parser = CodeParser(root_path)
        self.dependency_parser = DependencyParser(root_path)
        self.summary_parser = ProjectSummary(root_path)

    def analyze(self):

        return {

            "structure": self.repo_parser.get_project_structure(),

            "code": self.code_parser.parse(),

            "dependencies": self.dependency_parser.parse(),

            "summary": self.summary_parser.generate()

        }
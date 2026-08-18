from app.tools.code_parser import CodeParser
from app.services.dependency_service import DependencyService
from app.services.call_graph_service import CallGraphService

class RepositoryService:

    def __init__(self):

        self.parser = CodeParser(".")
        self.dependency = DependencyService(".")
        self.call_graph = CallGraphService(".")

    def get_repository_context(self):

        project = self.parser.parse()

        dependencies = self.dependency.analyze()

        context = ""

        context += "PROJECT FILES\n\n"

        for item in project:

            context += f"File : {item['file']}\n"

            context += f"Total Lines : {item['lines']}\n\n"

            context += "Classes\n"

            if item["classes"]:

                for cls in item["classes"]:

                    context += f"   {cls['name']} (Line {cls['line']})\n"

            else:

                context += "   None\n"

            context += "\nFunctions\n"

            if item["functions"]:

                for func in item["functions"]:

                    context += (
                        f"   {func['name']} "
                        f"(Line {func['line']}) "
                        f"Args: {func['args']}\n"
                    )

            else:

                context += "   None\n"

            context += "\nImports\n"

            if item["imports"]:

                for imp in item["imports"]:

                    context += f"   {imp}\n"

            else:

                context += "   None\n"

            context += "\n---------------------------------\n\n"

            context += "\nCALL GRAPH\n\n"

            graph = self.call_graph.analyze()

            for function, calls in graph.items():

                    context += f"{function}()\n"

                    if calls:

                        for call in calls:

                            context += f"   -> {call}()\n"

                    else:

                        context += "   -> None\n"

                    context += "\n"

        return context
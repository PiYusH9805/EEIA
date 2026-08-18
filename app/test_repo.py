from app.tools.repo_parser import RepositoryParser

parser = RepositoryParser(".")

files = parser.get_project_structure()

for file in files:
    print(file)
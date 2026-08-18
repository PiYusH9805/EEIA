from app.tools.dependency_parser import DependencyParser

parser = DependencyParser(".")

dependencies = parser.parse()

for item in dependencies:

    print("=" * 60)

    print("File :", item["file"])

    print("Imports:")

    if item["imports"]:

        for imp in item["imports"]:
            print("   -", imp)

    else:
        print("   No imports")
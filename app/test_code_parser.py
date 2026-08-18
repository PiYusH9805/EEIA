from app.tools.code_parser import CodeParser

parser = CodeParser(".")

result = parser.parse()

for file in result:

    print("=" * 60)

    print("File :", file["file"])

    print("Classes :")

    for c in file["classes"]:
        print("  -", c)

    print("Functions :")

    for f in file["functions"]:
        print("  -", f)

    print("Imports :")

    for i in file["imports"]:
        print("  -", i)
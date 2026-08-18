from app.services.code_service import CodeService

service = CodeService(".")

result = service.analyze()

print("=" * 60)
print("PROJECT SUMMARY")
print("=" * 60)

for key, value in result["summary"].items():

    print(f"{key:20}: {value}")

print("\n")

print("=" * 60)
print("PROJECT FILES")
print("=" * 60)

for file in result["structure"][:20]:

    print(file)
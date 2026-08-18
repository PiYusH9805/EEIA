from app.tools.project_summary import ProjectSummary

summary = ProjectSummary(".")

result = summary.generate()

print("\n========== EEIA Project Summary ==========\n")

for key, value in result.items():

    print(f"{key:20}: {value}")
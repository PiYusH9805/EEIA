from app.agents.planner.planner import PlannerAgent

planner = PlannerAgent()

while True:

    question = input("\nQuestion : ")

    if question.lower() == "exit":
        break

    answer = planner.route(question)

    print("\n")
    print(answer)
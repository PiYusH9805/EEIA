from app.agents.planner.planner import PlannerAgent

planner = PlannerAgent()

while True:

    q = input("\nQuestion : ")

    if q.lower() == "exit":
        break

    print()

    print(planner.route(q))
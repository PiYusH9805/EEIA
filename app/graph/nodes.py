from app.agents.planner.planner import PlannerAgent

planner = PlannerAgent()


def planner_node(state):

    question = state["question"]

    answer = planner.route(question)

    return {

        "question": question,

        "answer": answer

    }
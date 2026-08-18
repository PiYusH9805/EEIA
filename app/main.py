from app.agents.planner.planner import PlannerAgent

planner = PlannerAgent()


def chat(question: str):

    return planner.route(question)


def upload_document(uploaded_file):

    return planner.router.upload_document(uploaded_file)
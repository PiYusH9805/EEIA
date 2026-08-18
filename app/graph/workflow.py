from langgraph.graph import StateGraph

from app.graph.state import AgentState

from app.graph.nodes import planner_node


workflow = StateGraph(AgentState)

workflow.add_node(

    "planner",

    planner_node

)

workflow.set_entry_point(

    "planner"

)

workflow.set_finish_point(

    "planner"

)

graph = workflow.compile()
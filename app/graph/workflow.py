from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import planner_node, retrieve_node, agent_node, next_step, report_node

workflow = StateGraph(AgentState)
workflow.add_node('planner', planner_node)
workflow.add_node('retrieve', retrieve_node)
workflow.add_node('agent', agent_node)
workflow.add_node('report', report_node)
workflow.set_entry_point('planner')
workflow.add_edge('planner', 'retrieve')
workflow.add_edge('retrieve', 'agent')
workflow.add_conditional_edges('agent', next_step, {'agent': 'agent', 'report': 'report'})
workflow.add_edge('report', END)
graph = workflow.compile()

from langgraph.graph import StateGraph, END
from .state import TripState
from .nodes import agent_node, tool_node, should_continue

# Define Graph
workflow = StateGraph(TripState)

# Add Nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Set Entry Point
workflow.set_entry_point("agent")

# Add Edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

workflow.add_edge("tools", "agent")

# Compile
app = workflow.compile()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .state import TripState
from .tools import TOOLS

# Initialize Model
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(TOOLS)

# --- Nodes ---

async def agent_node(state: TripState):
    """
    Decides the next action (call tool or end).
    """
    messages = state["messages"]
    # If no system message, add one
    if not messages or not isinstance(messages[0], SystemMessage):
        sys_msg = SystemMessage(content="""You are a smart Trip Planner Assistant. 
        Your goal is to help users plan their trips by providing weather updates, finding places, checking flights, and suggesting hotels.
        
        CONTEXT:
        Source: {state.get("source", "Unknown")}
        Destination: {state.get("destination", "Unknown")}
        
        TOOLS AVAILABLE:
        - search_places: Find places/coordinates.
        - get_weather: Check weather.
        - get_flight_status: Check flights.
        - search_hotels: Find hotels.
        
        INSTRUCTIONS:
        1. When asked for "Place Details" or "Analysis", ALWAYS check Weather first, then provide a summary.
        2. Be concise and helpful.
        3. Determine "Best Time to Visit" based on weather and general knowledge.
        4. When asked for "Hotels" or "Accommodation", ALWAYS use the `search_hotels` tool. Never make up hotel lists. Return the results in a beautiful Markdown Table with columns: Hotel Name, Rating, Address.
        5. When asked for "Flights", first determine the IATA codes for the cities (e.g. Goa -> GOI). Then use `get_flight_status` with IATA codes. Return the results in a beautiful Markdown Table.
        """)
        # We handle system message logic carefully with Gemini (sometimes needs 1st message)
        # For simplicity in LangGraph, we just let the LLM see the history.
        pass

    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

from langgraph.prebuilt import ToolNode

# Use Prebuilt ToolNode (Standard in new LangGraph)
# We export it as 'tool_node' so graph.py can use it directly as a node.
tool_node = ToolNode(TOOLS)

def should_continue(state: TripState):
    """
    Conditional edge logic.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

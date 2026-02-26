import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

# Load Env
load_dotenv()

# Import Agent
from agent.graph import app as agent_app

app = FastAPI(title="Trip Planner Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AgentRequest(BaseModel):
    message: str
    source: Optional[str] = None
    destination: Optional[str] = None
    place_context: Optional[str] = None

class AgentResponse(BaseModel):
    response: str
    intermediate_steps: Optional[List[Any]] = None

class SearchRequest(BaseModel):
    query: str

# Routes
@app.get("/")
def health_check():
    return {"status": "running", "agent": "TripPlanner v1.0"}

@app.post("/api/agent/invoke", response_model=AgentResponse)
async def invoke_agent(req: AgentRequest):
    """
    Main endpoint to talk to the Trip Planner Agent.
    """
    from langchain_core.messages import HumanMessage
    
    # Construct Inputs
    inputs = {
        "messages": [HumanMessage(content=req.message)],
        "source": req.source,
        "destination": req.destination,
        "current_place": req.place_context
    }
    
    try:
        # Run Graph
        result = await agent_app.ainvoke(inputs)
        
        # Extract Final Response
        messages = result["messages"]
        last_msg = messages[-1]
        
        return AgentResponse(response=last_msg.content)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_proxy(req: SearchRequest):
    """
    Direct proxy to Nominatim search tool.
    Returns JSON list of places.
    """
    from agent.tools import search_places_impl
    try:
        res_json = await search_places_impl(req.query)
        import json
        return json.loads(res_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

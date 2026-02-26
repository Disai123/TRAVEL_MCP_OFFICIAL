# Development Guide — Smart MCP Trip Planner
**Version:** 1.0
**Stack:** React (Frontend) + FastAPI + LangGraph (Backend)
**Date:** 2026-02-04

---

## 1. Project Structure

```
tripplanner/
├── backend/
│   ├── main.py                  # FastAPI entry point & API routes
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # API keys (GEMINI_API_KEY, etc.)
│   ├── .env.example             # Template for env vars
│   ├── travel_sample.csv        # Hotel dataset (SQLite/CSV)
│   └── agent/
│       ├── __init__.py
│       ├── graph.py             # LangGraph StateGraph definition
│       ├── nodes.py             # LangGraph node functions (planner, tools, model)
│       ├── state.py             # TripState TypedDict
│       └── tools.py             # MCP tool wrappers (search_places, get_weather, etc.)
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css            # Global styles (Glassmorphism, animations)
│       └── components/          # React components (Map, SmartCard, FlightOverlay, etc.)
└── run_app.ps1                  # PowerShell script to start both servers
```

---

## 2. Backend Implementation

### 2.1 Environment Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

**`.env` file:**
```
GEMINI_API_KEY=your_gemini_api_key_here
AVIATIONSTACK_API_KEY=your_aviationstack_key_here
```

### 2.2 Key Backend Files

#### `agent/state.py` — TripState
```python
from typing import TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage
import operator

class TripState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    source: Optional[str]
    destination: Optional[str]
    current_place: Optional[str]
```

#### `agent/graph.py` — LangGraph StateGraph
```python
from langgraph.graph import StateGraph, END
from .state import TripState
from .nodes import call_model, call_tools, should_continue

workflow = StateGraph(TripState)
workflow.add_node("model", call_model)
workflow.add_node("tools", call_tools)
workflow.set_entry_point("model")
workflow.add_conditional_edges("model", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "model")
app = workflow.compile()
```

#### `agent/tools.py` — MCP Tool Wrappers
- `search_places_impl(query)` → calls Nominatim OSM API for famous places
- `get_weather_impl(location)` → calls Open-Meteo API for real-time weather
- `get_flight_status_impl(source, dest)` → calls AviationStack for flight data
- `search_hotels_impl(destination)` → queries local CSV/SQLite for hotels

#### `main.py` — FastAPI Routes
- `GET /` → health check
- `POST /api/agent/invoke` → main agent endpoint (receives `{message, source, destination, place_context}`)
- `POST /api/search` → direct Nominatim proxy for map search

---

## 3. Frontend Implementation

### 3.1 Setup
```bash
cd frontend
npm install
npm run dev      # Starts at http://localhost:5173
```

### 3.2 Key Components

| Component | Responsibility |
| :--- | :--- |
| `App.jsx` | Root — manages global Source/Destination state (React Context) |
| `LandingPage.jsx` | Screen 1: Source input with animated entry |
| `MapDashboard.jsx` | Screen 2: react-leaflet map with destination search |
| `SmartCard.jsx` | Screen 3: Slide-in drawer for place details (weather + AI insights) |
| `FlightOverlay.jsx` | Screen 4: Bottom sheet for flight results |
| `HotelExplorer.jsx` | Screen 5: Hotel grid/map with AI analysis popup |

### 3.3 API Call Pattern (Axios)
```javascript
// Invoke the LangGraph agent
const response = await axios.post('http://localhost:8000/api/agent/invoke', {
  message: `Tell me about ${placeName}`,
  source: sourceCity,
  destination: destinationCity,
  place_context: placeName
});
const agentReply = response.data.response;
```

### 3.4 Glassmorphism CSS Pattern
```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

---

## 4. Running the Full Application

```powershell
# Option 1: Use the PowerShell script
.\run_app.ps1

# Option 2: Manual startup
# Terminal 1 — Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev
```

- **Backend API:** http://localhost:8000
- **Frontend App:** http://localhost:5173

---

## 5. Coding Standards & Best Practices

- **Backend:** Follow PEP8; use `async/await` throughout; never hardcode API keys
- **Frontend:** Functional components only; use `useContext` for global state; avoid prop drilling
- **Error Handling:** Every API call must have try/catch; display user-friendly fallback messages
- **Performance:** Debounce search inputs (300ms); cache agent responses per session to avoid repeat LLM calls

---

## 📋 Development / Coding Prompt

> **How to use:** Copy the prompt below and paste it into Antigravity. Replace the placeholders with your project details. The AI will generate the complete full-stack code for your project.

```
I want to build a full-stack AI-powered web application called "[Your App Name]".

The app allows users to:
- Input [describe primary user input, e.g. "a source city and destination city"]
- See results on [describe the main display, e.g. "an interactive map", "a dashboard", "a results list"]
- Get real-time data from [describe your data sources, e.g. "weather API, flights API, hotels database"]
- Receive AI-generated insights from Google Gemini (LLM) based on the fetched data

Tech Stack:
- Frontend: React 18 (Vite), [add domain-specific libraries, e.g. "react-leaflet for maps"], Axios, framer-motion
- Backend: FastAPI (Python), LangGraph for agentic orchestration, LangChain + Google Gemini LLM
- Styling: Premium Glassmorphism — dark background, vibrant accent color for CTAs, glass cards with backdrop-blur

Generate the following files:

### Backend

1. `state.py` — Define a TypedDict state class with:
   - `messages`: Annotated list of BaseMessage (operator.add)
   - Fields for each key piece of user context (e.g. source, destination, selected item)

2. `tools.py` — Create one async tool function per data source using @tool decorator:
   - Tool 1: [describe first API — inputs, API endpoint, what it returns]
   - Tool 2: [describe second data source — inputs, query method, what it returns]
   - Tool 3: [add more as needed]

3. `nodes.py` — Three LangGraph node functions:
   - `call_model`: Bind Gemini (gemini-1.5-flash) with tools, write a system prompt describing the AI's role, invoke with current messages, return updated state
   - `call_tools`: Execute tool calls from last AI message using ToolNode pattern
   - `should_continue`: If last message has tool_calls → return "tools", else → return END

4. `graph.py` — Compile LangGraph StateGraph:
   - Nodes: "model" and "tools"
   - Entry: "model", conditional edges from "model" via should_continue, "tools" loops back to "model"
   - Export as `app = workflow.compile()`

5. `main.py` — FastAPI app:
   - CORS middleware (allow all origins for dev)
   - Pydantic request model with `message` (str) and optional context fields
   - GET "/" → health check
   - POST "/api/agent/invoke" → build state inputs, call `await agent_app.ainvoke(inputs)`, return last message content
   - POST "/api/search" → call the search tool directly, return parsed JSON
   - Wrap all routes in try/except with HTTPException

6. `requirements.txt`: fastapi, uvicorn, python-dotenv, langchain, langchain-google-genai, langgraph, langchain-core, httpx, pandas, requests

### Frontend

7. `App.jsx` — Root with React Context holding all global state (user inputs + current screen). Renders different screens based on state.

8. Screen components (one per major user flow step):
   - Screen 1 [Landing/Input]: Full-screen background, glassmorphism center card, user enters their primary input, animated Next button
   - Screen 2 [Main View]: [describe: map / list / dashboard] showing fetched results, search bar, persistent context pill
   - Screen 3 [Detail View]: Slide-in panel (framer-motion) triggered by clicking a result — shows AI-generated insights + data from APIs
   - Screen 4 [Secondary Data]: Modal/bottom-sheet for secondary data (e.g. flights, recommendations), scrollable cards, empty state message
   - Screen 5 [Action Screen]: Grid of options (e.g. hotels, products), AI analysis popup, external CTA button ("Book Now" or equivalent)

9. `index.css` — Global styles:
   - Import Google Fonts (Inter + one display font)
   - CSS custom properties for colors
   - `.glass-card` class: rgba background, backdrop-filter blur, border, border-radius
   - Shimmer skeleton animation
   - Button hover glow effect
   - All interactions: transition: all 0.3s ease

Important requirements:
- Backend URL: http://localhost:8000
- Show loading states ("Thinking...", shimmer skeleton) on all API calls
- Graceful error fallbacks on every fetch (never crash the UI)
- The primary user context (first input) must persist and appear on every subsequent screen without re-entering
- Design must feel premium — dark, glassmorphic, animated
```

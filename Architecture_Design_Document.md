# Architecture Design Document (ADD)
**Project:** Smart MCP Trip Planner
**Version:** 1.1 (Agentic)
**Date:** 2026-02-04

---

## 1. System Overview
The **Smart MCP Trip Planner** is a distributed web application designed to provide a unified travel planning experience. It uses **LangGraph** to orchestrate an Agentic workflow that intelligently selects MCP tools and processes data.

### 1.1 High-Level Diagram
```mermaid
graph TD
    Client[Client Browser (React SPA)] <-->|REST API (JSON)| Backend[Backend API (FastAPI)]
    
    subgraph "Backend Orchestration Layer (LangGraph)"
        Backend -->|State| Agent_Graph[LangGraph StateGraph]
        Agent_Graph -->|Decision| Router[LLM Router]
        Router -->|Action| Tool_Node[Tool Execution Node]
        Router -->|Synthesis| Final_Node[Response Generator]
    end
    
    subgraph "Data & Tool Layer (MCP Servers)"
        Tool_Node <-->|SSE / Stdio| OSM_Server[OSM Server (Weather, Maps, Flights)]
        Tool_Node <-->|SSE / Stdio| Travel_Server[Travel Server (Hotels Database)]
    end
    
    OSM_Server <-->|HTTP| External_APIs[Open-Meteo, AviationStack, Nominatim]
    Travel_Server <-->|SQL| Hotel_DB[(SQLite / CSV)]
```

---

## 2. Component Architecture

### 2.1 Frontend (Presentation Layer)
- **Framework:** React 18+ (Vite Build Tool)
- **Language:** JavaScript (ES6+) / JSX
- **State Management:** React Context API (Global Store for Source/Dest).
- **Mapping:** `react-leaflet`.
- **API Client:** Axios.

### 2.2 Backend (Application Layer)
- **Framework:** FastAPI (Python 3.10+)
- **Concurrency:** `asyncio`.
- **Orchestration:** **LangGraph** (Agentic State Management).
- **Interface:** RESTful API (JSON).

**Key Modules:**
- `main.py`: Entry point, API routes invoke Agent Graph.
- `agent.py`: Defines the LangGraph `StateGraph`, Nodes (`planner`, `tools`, `model`), and State (`TripState`).
- `mcp_wrapper.py`: Wraps MCP tool calls into LangChain-compatible `StructuredTool`.
- `models.py`: Pydantic models.

### 2.3 Data & Tool Layer (MCP)
The Agent has access to the following tools:
1.  **OSM Server**: `search_places`, `get_weather`, `get_flight_status`.
2.  **Travel Server**: `search_hotels`.

### 2.4 AI Layer (LangGraph Agent)
- **Provider:** Google Gemini (via `langchain-google-genai`).
- **Role:** Agent Brain (Reasoning & Tool Selection).
- **Workflow (Agentic):**
    1.  **State Initialization**: Backend initializes `TripState` with `{source, destination, current_place}`.
    2.  **Node execution**: LangGraph executes nodes:
        -   **Routing**: Determines if Tools are needed (e.g., "Get Weather") or if it can answer directly.
        -   **Tool Execution**: Calls the MCP tools via the wrapper.
        -   **Reflection/Synthesis**: Aggregates tool outputs into a cohesive response.
    3.  **Final Output**: Returns proper JSON structure for the Frontend widgets.

---

## 3. Data Flow

### Scenario: User checks "Place Details"
1.  **Frontend**: `GET /api/agent/details?place=TajMahal`.
2.  **Backend Agent**:
    -   Receives `messages=[User: "Tell me about Taj Mahal"]`.
    -   **Step 1**: Agent calls `get_weather("Taj Mahal")`.
    -   **Step 2**: Agent calls `llm` with weather data to generate "Best time to visit".
    -   **Step 3**: Agent formats output to JSON.
3.  **Frontend**: Display Weather Widget and AI Text.

---

## 4. Technical Stack Summary

| Layer | Technology | Version / Ref |
| :--- | :--- | :--- |
| **Frontend** | React, Vite | Latest |
| **Backend** | FastAPI | v0.100+ |
| **Orchestration** | **LangChain / LangGraph** | Latest |
| **Runtime** | Python | v3.10+ |
| **LLM** | Google Gemini | `langchain-google-genai` |
| **Tools** | MCP SDK | `mcp` |

---

## 5. Deployment & Security
- **Dev Environment**:
    -   Frontend: `npm run dev` (Port 5173).
    -   Backend: `uvicorn main:app --reload` (Port 8000).
-   **Security**:
    -   API Keys (AviationStack, Gemini) stored in `.env`.

---

## 📋 Architecture Design Document (ADD) Creation Prompt

> **How to use:** Copy the prompt below and paste it into Antigravity. Replace the placeholders with your project details. The AI will generate a full Architecture Design Document.

```
I am building a full-stack AI-powered web application called "[Your App Name]".

Create a professional Architecture Design Document (ADD) in Markdown for this project. The system must:
- Have a React frontend (Vite) communicating with a FastAPI Python backend via REST API
- Use LangGraph to orchestrate an agentic AI workflow on the backend
- Connect to 2 or more external data sources (APIs or databases) via tool functions
- Use Google Gemini as the LLM (via langchain-google-genai)

The ADD must contain these sections:

1. **System Overview**
   - A brief description of the system as a distributed web application with an agentic orchestration layer
   - A Mermaid architecture diagram showing all layers:
     - Client (React SPA) ↔ REST API ↔ Backend (FastAPI)
     - Backend Orchestration Layer: LangGraph StateGraph → LLM Router Node → Tool Execution Node → Response Generator Node
     - Data/Tool Layer: Each external data source or server with its protocol (HTTP/SQL/Stdio)
     - Each external data source connected to its API or database

2. **Component Architecture** — describe each layer in detail:
   - **Frontend**: Framework, language, state management approach, mapping/UI libraries, API client
   - **Backend**: Framework, concurrency model, orchestration tool, API interface style, list of key Python modules and what each does
   - **Tool/Data Layer**: List each tool function, what API or database it calls, and what data it returns
   - **AI Layer**: LLM provider, its role (reasoning + tool selection), the agentic workflow steps (State Init → Node Execution → Final Output)

3. **Data Flow** — walk through one concrete end-to-end scenario:
   - Show exactly what happens from a frontend API call → backend agent → tool calls → LLM synthesis → response to frontend
   - Number each step clearly

4. **Technical Stack Summary** as a table:
   - One row per layer: Frontend, Backend, Orchestration, Runtime, LLM, Tools/SDKs

5. **Deployment & Security**:
   - Dev environment startup commands for frontend and backend
   - How API keys are stored and accessed (environment variables via .env)

Format with Markdown headings, a Mermaid diagram code block, tables, and horizontal rules. Tone should be technical and precise, suitable for a software architect or senior developer.
```


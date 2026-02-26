# Testing & Deployment Guide — Smart MCP Trip Planner
**Version:** 1.0
**Stack:** React (Frontend) + FastAPI + LangGraph (Backend)
**Date:** 2026-02-04

---

## 1. Testing Strategy

### 1.1 Testing Levels

| Level | Scope | Tools |
| :--- | :--- | :--- |
| **Unit Tests** | Individual Python functions (tools, nodes) | `pytest`, `pytest-asyncio` |
| **Integration Tests** | API endpoints end-to-end | `httpx` / FastAPI `TestClient` |
| **Frontend Tests** | React component behavior | `Vitest`, `React Testing Library` |
| **Manual / E2E Tests** | Full user flow in browser | Browser + checklists |

---

## 2. Backend Testing

### 2.1 Unit Tests — Tools

**Test: `search_places_impl`**
```python
# tests/test_tools.py
import pytest
from agent.tools import search_places_impl

@pytest.mark.asyncio
async def test_search_places_returns_results():
    result = await search_places_impl("Bangalore")
    import json
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "lat" in data[0]
    assert "lon" in data[0]
```

**Test: `get_weather_impl`**
```python
@pytest.mark.asyncio
async def test_get_weather_returns_string():
    result = await get_weather_impl("Mumbai")
    assert isinstance(result, str)
    assert "temperature" in result.lower() or "°" in result
```

**Test: `search_hotels_impl`**
```python
@pytest.mark.asyncio
async def test_search_hotels_for_valid_city():
    result = await search_hotels_impl("Goa")
    import json
    data = json.loads(result)
    assert isinstance(data, list)
```

### 2.2 Integration Tests — API Endpoints

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_agent_invoke_valid():
    payload = {
        "message": "Tell me about Taj Mahal",
        "source": "Delhi",
        "destination": "Agra",
        "place_context": "Taj Mahal"
    }
    response = client.post("/api/agent/invoke", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()
    assert len(response.json()["response"]) > 0

def test_agent_invoke_empty_message():
    response = client.post("/api/agent/invoke", json={"message": ""})
    assert response.status_code in [200, 422]

def test_search_proxy_valid():
    response = client.post("/api/search", json={"query": "Coorg"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 2.3 Running Backend Tests
```bash
cd backend
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

---

## 3. Frontend Testing

### 3.1 Component Tests

**Test: `LandingPage` Source Input**
```javascript
// src/components/__tests__/LandingPage.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import LandingPage from '../LandingPage';

test('renders source input and next button', () => {
  render(<LandingPage onNext={() => {}} />);
  expect(screen.getByPlaceholderText(/starting from/i)).toBeInTheDocument();
  expect(screen.getByText(/next/i)).toBeInTheDocument();
});

test('calls onNext with source value on submit', () => {
  const mockOnNext = jest.fn();
  render(<LandingPage onNext={mockOnNext} />);
  fireEvent.change(screen.getByPlaceholderText(/starting from/i), {
    target: { value: 'Bangalore' }
  });
  fireEvent.click(screen.getByText(/next/i));
  expect(mockOnNext).toHaveBeenCalledWith('Bangalore');
});
```

### 3.2 Running Frontend Tests
```bash
cd frontend
npm install
npm test          # Runs Vitest in watch mode
npm run test:run  # Single CI run
```

---

## 4. Manual E2E Test Checklist

### Flow 1: Full Trip Planning Flow ✅
- [ ] Open app at http://localhost:5173
- [ ] Enter "Bangalore" as Source → Click Next
- [ ] Type "Coorg" in destination search → Map pans to Coorg
- [ ] Markers appear for famous places (e.g., Abbey Falls)
- [ ] Click a marker → Smart Card slides in
- [ ] Smart Card shows Weather (temperature + wind)
- [ ] Smart Card shows AI insights (best time, travel duration, transport hubs)
- [ ] Click "Show Flights" → Flight overlay appears
- [ ] Flight cards display or empty state shows
- [ ] Click "Find Hotels" → Hotel grid loads
- [ ] Click a hotel → AI analysis popup appears
- [ ] Click "Book Now" → External MakeMyTrip link opens

### Flow 2: Error & Edge Cases ✅
- [ ] Enter unknown destination → Map shows error or stays at default
- [ ] API failure (stop backend) → Frontend shows fallback message (no crash)
- [ ] Enter Source with special characters → Handles gracefully
- [ ] Source label "Starting from: [Source]" persists on Map and Hotel screens

---

## 5. Deployment Guide

### 5.1 Local Development
```powershell
# From the tripplanner/ root directory
.\run_app.ps1
```
Or manually:
```bash
# Terminal 1
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev
```

### 5.2 Production Deployment on Render

#### Backend (FastAPI) — Render Web Service
1. Push your `backend/` folder to a GitHub repository.
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo.
3. Set the following:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment** tab, add:
   - `GEMINI_API_KEY` = your Gemini API key
   - `AVIATIONSTACK_API_KEY` = your AviationStack key
5. Click **Deploy** — Render will build and host the backend. Copy the public URL (e.g. `https://tripplanner-api.onrender.com`).

#### Frontend (React) — Render Static Site
1. Build the production bundle locally:
   ```bash
   cd frontend
   npm run build
   ```
2. Go to Render → **New Static Site** → connect your repo.
3. Set the following:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Under **Environment** tab, add:
   - `VITE_API_BASE_URL` = your Render backend URL from step 5 above
5. Click **Deploy** — Render hosts the frontend as a static site.

> ⚠️ **Important:** Update all `http://localhost:8000` references in your frontend code to use `import.meta.env.VITE_API_BASE_URL` before deploying.

### 5.3 Environment Variables Quick Reference

| Variable | Required | Where Set | Description |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | ✅ Yes | Render Backend Env | Powers LLM calls via Gemini |
| `AVIATIONSTACK_API_KEY` | ✅ Yes | Render Backend Env | Powers flight search |
| `VITE_API_BASE_URL` | ✅ Production | Render Frontend Env | Points frontend to backend URL |

---

## 📋 Testing & Deployment Prompt

> **How to use:** Copy the prompt below and paste it into Antigravity. Replace the placeholders with your project details. The AI will generate a complete Testing & Deployment Guide for your project.

```
I have built a full-stack AI-powered web application called "[Your App Name]" with:
- Frontend: React (Vite) — components include [list your main components, e.g. LandingPage, MapDashboard, SmartCard]
- Backend: FastAPI + LangGraph — tool functions include [list your tools, e.g. search_places, get_weather, search_hotels]
- The app is served at: frontend on localhost:5173, backend on localhost:8000

Create a complete Testing & Deployment Guide in Markdown. The guide must include:

1. **Testing Strategy** — a table with 4 levels:
   - Unit Tests (pytest + pytest-asyncio for Python tool functions)
   - Integration Tests (FastAPI TestClient for API endpoints)
   - Frontend Tests (Vitest + React Testing Library for components)
   - Manual E2E Tests (browser-based checklist)

2. **Backend Unit Tests** — write actual pytest code for:
   - One test per tool function: call it with a valid input, assert the return type and key fields in the result
   - Use `@pytest.mark.asyncio` for async tool functions
   - Save to `tests/test_tools.py`
   - Include the command to run: `pytest tests/ -v`

3. **Backend Integration Tests** — write actual TestClient code for:
   - GET "/" → health check (status 200, correct status field)
   - POST "/api/agent/invoke" with a valid message and context fields → status 200, non-empty response field
   - POST "/api/agent/invoke" with an empty message → should not crash (200 or 422)
   - POST "/api/search" with a valid query → status 200, returns a list
   - Save to `tests/test_api.py`

4. **Frontend Component Tests** — write actual test code (Vitest syntax) for the first two UI components:
   - Test 1: Renders the main input field and action button
   - Test 2: Calls the onNext/onSubmit callback with the entered value when button is clicked

5. **Manual E2E Test Checklist** — two checkbox lists:
   - Happy Path: tick through every step of the full user journey from first input to final action (book/confirm/output)
   - Edge Cases: unknown input, backend down/API failure (no UI crash), special characters, context persistence across screens

6. **Deployment Guide on Render** covering:
   - Local dev: exact terminal commands to start frontend and backend
   - Backend on Render Web Service: Root Directory, Build Command (`pip install -r requirements.txt`), Start Command (`uvicorn main:app --host 0.0.0.0 --port $PORT`), and which env vars to add
   - Frontend on Render Static Site: Root Directory, Build Command (`npm install && npm run build`), Publish Directory (`dist`), and VITE_API_BASE_URL env var pointing to the backend URL
   - Note: remind the user to replace all `localhost:8000` references with `import.meta.env.VITE_API_BASE_URL` in frontend code
   - Environment Variables table: variable name, required or optional, where it is set (Render backend / Render frontend)

Format with clear Markdown headings, fenced code blocks (python, javascript, bash), checkbox lists, and tables. Tone should be practical and developer-friendly.
```

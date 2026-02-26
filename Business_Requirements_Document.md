# Business Requirement Document (BRD)
**Project Name:** Smart MCP Trip Planner
**Version:** 1.0
**Date:** 2026-02-04

---

## 1. Introduction

### Purpose
The purpose of this document is to define the business requirements for the **Smart MCP Trip Planner**, a web application designed to assist users in planning trips by integrating real-time data services (Model Context Protocol - MCP) and Large Language Model (LLM) intelligence.

### Background
Travel planning often involves juggling multiple platforms for maps, weather, flights, and hotels. The Stakeholder currently has distinct MCP tools for these functions. The goal is to consolidate these into a unified, "End-to-End" flow that provides a seamless user experience, enriched by AI recommendations.

### Project Scope
The project entails building a modern web application using **React (Frontend)** and **FastAPI (Backend)**.
- **In Scope:**
    - User interface for selecting Source and Destination.
    - Interactive Maps for visualizing destinations.
    - Real-time fetching of Weather, Flight Status, and Hotel availability via MCP servers.
    - AI-driven insights (Best time to visit, travel time estimation, distance to transit hubs).
    - Redirection to external booking platforms (e.g., MakeMyTrip).
- **Out of Scope:**
    - Direct payment processing (Booking happens externally).
    - User account management/Login system (MVP focus).

### Objectives
1.  **Unified Experience:** Eliminate context switching by bringing Map, Weather, Flight, and Hotel data into one flow.
2.  **Context Retention:** "Source" location is fixed once entered and used contextually throughout the session.
3.  **AI Enrichment:** Use LLMs to provide qualitative data that APIs miss (e.g., "Best time to visit", "Distance to Airport").

---

## 2. Business Requirements

### Functional Requirements (FR)

**FR-01: Source Selection (The "Anchor")**
- The system must capture the User's "Source" location at the start of the session.
- This Source location must be persisted and used for all subsequent distance and flight calculations.

**FR-02: Destination Discovery & Mapping**
- The system must allow users to search for a Destination city.
- The system must display an interactive map showing famous places in the selected destination (via OSM MCP).
- **Interactive Element:** Clicking a place on the map must trigger a details card/sidebar.

**FR-03: Place Details & Weather**
- Upon selecting a place, the system must fetch real-time weather using the Weather MCP.
- The system must use an LLM to generate:
    - Best time to visit.
    - Estimated hours to reach from the Source.
    - Nearest Railway Station, Bus Station, and Airport with distances.

**FR-04: Flight Search**
- The system must provide a "Show Flights" feature.
- It must fetch flight status/options between the Source and Destination using the Flight MCP.
- Results must be displayed in a uniform card layout.

**FR-05: Hotel Search & AI Analysis**
- The system must allow users to "Book Hotels" at the Destination.
- It must fetch a list of hotels using the Hotel MCP.
- **Deep Dive:** When a user views hotel details, the LLM must analyze its location relative to the specific transport hubs found in FR-03.
- **Booking Action:** Clicking "Book Now" must redirect the user to the booking provider (e.g., MakeMyTrip).

### Non-Functional Requirements (NFR)
- **Performance:** MCP tool calls should return results within 3-5 seconds; LLM responses should be streamed or returned within 5-8 seconds to maintain engagement.
- **Reliability:** The system must handle API failures (e.g., external weather service down) gracefully, showing cached or fallback messages.
- **Usability:** The UI must be "Beautiful" and "Premium" (Responsive, Glassmorphism, Smooth Transitions) as per user design standards.
- **Scalability:** The Backend (FastAPI) should be stateless to allow easy scaling of user sessions.

### Constraints and Assumptions
- **Architecture:** Must use React (Frontend) and FastAPI (Backend).
- **Data Source:** Primary data comes from `osm_server.py` and `travel_server.py` (MCP).
- **LLM Limits:** identifying specific distances relies on LLM knowledge base or OSM calculations; specific "live" distance calculation might be approximated by the LLM if not available via API.

---

## 3. Stakeholders and Roles

| Role | Responsibility |
| :--- | :--- |
| **Product Owner (User)** | Define vision, approve designs, and validate the end-to-end flow. |
| **Business Analyst (AI)** | Document requirements, define process flows, and bridging technical gaps. |
| **Developer (AI/User)** | Implement Frontend (React) and Backend (FastAPI) code. |
| **End User** | The traveler interacting with the application. |

---

## 4. Process Flows / Use Cases

### User Story: "The Weekend Getaway"
1.  **Start:** User enters "Bangalore" as **Source**.
2.  **Search:** User enters "Coorg" as **Destination**.
3.  **View:** Map loads with markers for "Abbey Falls", "Raja's Seat".
4.  **Interact:** User clicks "Abbey Falls".
5.  **Insight:** Side panel shows:
    - *Weather:* "22°C, Cloudy"
    - *AI Advice:* "Best visited Monsoons. ~5-6 hours drive from Bangalore."
6.  **Flights:** User checks flights (System shows "No direct flights, nearest airport Mangalore").
7.  **Hotels:** User clicks "Find Hotels". List appears. User checks "Coorg Wilderness Resort".
8.  **Detail:** AI says "Resort is 4km from Bus Stand."
9.  **Action:** User clicks "Book", redirects to MakeMyTrip.

---

## 5. Data Requirements

| Data Entity | Source | Storage/Session |
| :--- | :--- | :--- |
| **Source Location** | User Input | Session State (React Context) |
| **Destination** | User Input | Session State |
| **Map Coordinates** | OSM MCP | Temporary (Map Render) |
| **Weather Data** | Open-Meteo (OSM MCP) | cached on view |
| **Flight Status** | AviationStack (OSM MCP) | cached on view |
| **Hotel Inventory** | SQLite/CSV (Travel DB) | Query on demand |

---

## 6. Success Metrics / Acceptance Criteria
- [ ] **Flow Completion:** A user can go from Source Input -> Destination Map -> Hotel Booking Link without error.
- [ ] **Context Awareness:** The "Source" location does not need to be re-entered at the Flight stage.
- [ ] **AI Accuracy:** LLM recommendations (e.g., nearest airport) are factually correct for major cities.
- [ ] **Latency:** Map renders within 2 seconds of search.

---

## 7. Risks and Mitigations

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **API Rate Limits** | High (Service Blockage) | Implement caching for frequent queries (Weather/Places). Use mock data for dev. |
| **LLM Hallucination** | Medium (Wrong Distances) | Prompt Engineering to restrict LLM to "approximate" or "general knowledge"; verify with MCP tools where possible. |
| **Map Data Gaps** | Low | Use generic fallback search if specific "Famous Places" aren't found. |

---

## 📋 BRD Creation Prompt

> **How to use:** Copy the prompt below and paste it into Antigravity. Replace `[Your Project Name]` and `[your domain]` with your own values. The AI will generate a full BRD for your project.

```
I am building a full-stack AI-powered web application called "[Your Project Name]" in the [your domain] domain (e.g., travel, healthcare, finance).

Create a professional Business Requirements Document (BRD) in Markdown format for this project. The application must:
- Accept inputs from the user (like a source and destination, or search criteria)
- Use real-time external data APIs (weather, maps, flights, hotels, or equivalent for your domain)
- Use an LLM (Google Gemini) to generate AI-powered insights from API data
- Have a React frontend and a FastAPI Python backend
- Follow a premium UI design (Glassmorphism, animations, dark theme)

The BRD must contain these sections:

1. **Introduction**
   - Purpose: What problem does this app solve? What value does it deliver?
   - Background: Why does this problem exist today (too many disconnected tools, manual effort, etc.)?
   - Project Scope:
     - In-Scope: List 4–6 core features the app will deliver
     - Out-of-Scope: List 2–3 features deliberately excluded from the MVP (e.g., payments, user accounts)
   - Objectives: 3 numbered goals covering user experience, data flow, and AI enrichment

2. **Business Requirements**
   - Functional Requirements (FR-01 through FR-05): Each covering one major feature, what triggers it, what data it fetches/generates, and what the user sees
   - Non-Functional Requirements: Performance targets, reliability/error handling, UI quality bar, scalability approach
   - Constraints & Assumptions: Tech stack constraints, data source dependencies, LLM limitations

3. **Stakeholders and Roles** (table format):
   - Product Owner, Business Analyst (AI), Developer (AI/User), End User

4. **Process Flows / Use Cases**
   - Write one detailed end-to-end user story (give it a relatable name) showing a real user completing the full flow step by step, from first input to final action

5. **Data Requirements** (table format):
   - For each major data entity, list: what it is, where it comes from, and how it's stored or passed

6. **Success Metrics / Acceptance Criteria** (checkbox list):
   - 4 measurable criteria that define "done" for this MVP

7. **Risks and Mitigations** (table format):
   - 3 risks with their impact level and concrete mitigation strategies

Format with clear Markdown headings, horizontal rules between sections, and professional tone suitable for a software project BRD.
```


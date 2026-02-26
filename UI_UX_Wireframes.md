# UI/UX Wireframe & Design Guidelines
**Project:** Smart MCP Trip Planner
**Framework:** React + Tailwind CSS
**Theme:** Premium, Glassmorphism, Modern Travel Aesthetic

---

## 1. Design System

### Color Palette
- **Primary:** `Deep Ocean Blue` (#0f172a) - Backgrounds
- **Accent:** `Sunset Orange` (#f97316) - Call to Actions (Buttons)
- **Glass:** `Rgba(255, 255, 255, 0.1)` with Backdrop Blur (10px) - Cards/Modals
- **Text:** `Slate-50` (White/Off-white) - Headings; `Slate-300` - Body

### Typography
- **Headings:** *Outfit* or *Inter* (Google Fonts) - Bold, Modern.
- **Body:** *Inter* - Clean, readable.

---

## 2. Screen Flows & Wireframes

### Screen 1: The Landing (Source Input)
**Layout:**
- Full-screen high-quality travel background image (dimmed).
- **Center Container (Glass Effect):**
    - **Header:** "Start Your Journey"
    - **Input:** Large, floating label input: "Where are you starting from?" (Source)
    - **Button:** "Next" (Arrow Icon, Animated).

**Interaction:**
- On Entry: Fade-in animation.
- User types -> Auto-complete (if feasible) -> Click Next -> Seamless transition to Map.

### Screen 2: The Map Dashboard (Main View)
**Layout:**
- **Background:** Full-screen interactive map (`react-leaflet`).
- **Top Bar (Floating Glass):**
    - Left: "Trip to..." (Editable Search Input for Destination).
    - Right: User Avatar / Settings.
- **Top Left Indicator:** "Starting from: [Source]" (Persistent context pill).

**State - Map Markers:**
- Pins drop on "Famous Places" in the destination city.
- Hover Effect: Marker scales up, shows tooltip name.

### Screen 3: The Smart Card (Place Details)
**Trigger:** User clicks a Marker on the Map.
**Layout (Right Sidebar / Drawer):**
- **Type:** Slide-in from right (Glassmorphism).
- **Header:** Place Name (e.g., "Eiffel Tower") + Image (Placeholder/generated).
- **Section 1: Weather (MCP):**
    - Icon (Sun/Cloud) + Temp (22°C) + Wind.
- **Section 2: AI Advisor (LLM):**
    - *"Best time: Mornings (9 AM)."*
    - *"Travel: 5h 20m from [Source]."*
    - *"Nearest Airport: CDG (40 mins)."*
- **Action Buttons (Bottom Fixed):**
    - [Show Flights] (Primary)
    - [Find Hotels] (Secondary)

### Screen 4: Flights Overlay
**Trigger:** Click "Show Flights" in Smart Card.
**Layout (Bottom Sheet / Modal):**
- **Header:** "Flights from [Source] to [Dest]"
- **Content:** Horizontal scroll listing of Flight Cards.
    - **Card:**
        - Airline Logo (Text/Icon).
        - Details: Dep Time -> Arr Time.
        - Status: "On Time" (Green).
- **Empty State:** "No direct flights found. Try nearest airport..."

### Screen 5: Hotel Explorer
**Trigger:** Click "Find Hotels".
**Layout:**
- **View:** Map zooms to Hotel markers OR Grid overlaps the map.
- **Grid Item (Card):**
    - Hotel Name.
    - Star Rating.
    - **Snippet:** "Click for AI Analysis".
- **Detail View (Pop-up):**
    - **AI Analysis:** *"Excellent location. 2km from City Center. 15km from Airport."*
    - **CTA:** "Book Now" (External Link icon).

---

## 3. Micro-Interactions (The "Wow" Factor)
1.  **Map Pan**: When searching a new destination, smooth fly-to animation.
2.  **Card Slide**: Sidebar shouldn't just appear; it should slide with a spring physics animation (`framer-motion`).
3.  **Loading States**: Instead of spinners, use "Shimmer" skeletons or meaningful text ("Asking the Travel Spirit...").
4.  **Hover Effects**: Buttons should glow or lift on hover.

---

## 📋 UI/UX Design Prompt

> **How to use:** Copy the prompt below and paste it into Antigravity. Replace the placeholders with your app's specifics. The AI will generate a full UI/UX Wireframe & Design Guidelines document.

```
I am building a React web application called "[Your App Name]" with a [describe your theme, e.g. travel, fintech, healthcare] theme.

Create a detailed UI/UX Wireframe and Design Guidelines document in Markdown. The design must be premium — use Glassmorphism, smooth animations, and a dark color theme.

The document must contain:

1. **Design System**
   - Color Palette: Choose a dark background color, a vibrant accent color for CTAs, a glass card color (rgba with blur), and text colors for headings vs body
   - Typography: Use Google Fonts — suggest a modern heading font and a clean body font

2. **Screen Flows & Wireframes** — describe each major screen of the app:
   For each screen, define:
   - What triggers this screen (user action or navigation)
   - Layout structure (full-screen map / center card / sidebar / grid / modal)
   - All visible UI elements (inputs, buttons, data cards, headers)
   - What data is displayed and where it comes from (API, LLM, user input)
   - Key interaction behavior (what happens on click/hover/submit)

   The screens should cover the full user journey:
   - Screen 1: Initial input / landing (user provides their main search criteria)
   - Screen 2: Main dashboard / results view (primary data display, map or list)
   - Screen 3: Detail view (clicking an item opens a contextual panel with AI insights)
   - Screen 4: Secondary data overlay (e.g., flights, related data, second API result)
   - Screen 5: Action / booking / output screen (final step with external link or confirmation)

3. **Micro-Interactions (The "Wow" Factor)**
   - Describe at least 4 animations or interaction effects that make the UI feel alive:
     e.g., fly-to map animation, slide-in panel, shimmer loading skeleton, button glow on hover

Format with clear headings, bullet points, and horizontal rules. Write in a tone suitable for a frontend developer or UI designer implementing the app.
```

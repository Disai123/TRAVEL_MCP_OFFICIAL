import httpx
import os
import json
import pandas as pd
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# --- GLOBAL RESOURCES ---
# Load CSV once on startup to avoid re-reading 37MB file on every request.
HOTEL_DF = None
try:
    if os.path.exists("travel_sample.csv"):
        HOTEL_DF = pd.read_csv("travel_sample.csv", encoding="ISO-8859-1", low_memory=False)
except Exception as e:
    print(f"Error loading CSV: {e}")

# --- HELPER FUNCTIONS (Internal Logic) ---

async def search_places_impl(query: str) -> str:
    """Internal implementation of Place Search."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 5}
    headers = {"User-Agent": "TripPlannerAgent/1.0"}
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, headers=headers)
            data = resp.json()
            if not data: return "[]"
            simplified = [{"name": p.get("display_name"), "lat": float(p.get("lat")), "lon": float(p.get("lon"))} for p in data]
            return json.dumps(simplified)
        except Exception as e:
            raise Exception(f"Nominatim Search Failed: {e}")

async def _get_weather_impl(location_name: str) -> str:
    """Internal implementation of Weather."""
    # 1. Geocode using internal function
    geo_res = await search_places_impl(location_name)
    try:
        places = json.loads(geo_res)
        if not places: return f"Could not find location: {location_name}"
        lat, lon = places[0]['lat'], places[0]['lon']
    except:
        return f"Error parsing location for weather: {location_name}"

    # 2. Weather
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
        curr = data.get("current", {})
        return f"Weather in {location_name}: {curr.get('temperature_2m')}°C, Wind {curr.get('wind_speed_10m')} km/h (Code {curr.get('weather_code')})"

async def _get_flight_status_impl(departure: str, arrival: str) -> str:
    api_key = os.getenv("AVIATIONSTACK_API_KEY")
    if not api_key: return "Error: Missing AviationStack API Key."
    
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": api_key,
        "dep_iata": departure, 
        "arr_iata": arrival,
        "limit": 5
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params)
            data = resp.json()
            if "error" in data: return f"API Error: {data['error']['info']}"
            flights = data.get("data", [])
            if not flights: return "No flights found."
            
            # Markdown Table Header
            table = "| Airline | Flight | Status |\n|---|---|---|\n"
            for f in flights:
                 table += f"| {f['airline']['name']} | {f['flight']['iata']} | {f['flight_status']} |\n"
            return table
        except Exception as e:
            return f"Error fetching flights: {e}"

async def _search_hotels_impl(city: str) -> str:
    try:
        if HOTEL_DF is None:
            return "Error: Database file not loaded."
        
        # Use global DF
        results = HOTEL_DF[HOTEL_DF['city'].str.contains(city, case=False, na=False)].head(5)
        
        if results.empty:
            return f"No hotels found for {city} in database."
        
        # Markdown Table Header
        table = "| Hotel Name | Rating | Address |\n|---|---|---|\n"
        for _, row in results.iterrows():
            name = row.get('property_name', 'Unknown')
            rating = row.get('hotel_star_rating', 'N/A')
            address = row.get('address', 'N/A').replace("|", ",") # Escape pipes
            table += f"| {name} | {rating} | {address} |\n"
        
        return table
    except Exception as e:
        return f"Error querying hotel database: {e}"

# --- EXPORTED TOOLS (Wrapped) ---

@tool
async def search_places(query: str) -> str:
    """Search for places using OpenStreetMap (Nominatim). Returns JSON list of name, lat, lon."""
    return await search_places_impl(query)

@tool
async def get_weather(location_name: str) -> str:
    """Get current weather for a location name. Returns details text."""
    return await _get_weather_impl(location_name)

@tool
async def get_flight_status(departure: str, arrival: str) -> str:
    """Get real-time flight status. IMPORTANT: Arguments strictly require 3-letter IATA Airport Codes (e.g., 'DEL', 'BOM', 'JFK'). Do NOT use city names."""
    return await _get_flight_status_impl(departure, arrival)

@tool
async def search_hotels(city: str) -> str:
    """Search for hotels in a city using the local travel database."""
    return await _search_hotels_impl(city)

TOOLS = [search_places, get_weather, get_flight_status, search_hotels]

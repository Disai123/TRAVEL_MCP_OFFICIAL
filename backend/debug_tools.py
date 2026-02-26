import asyncio
import os
from dotenv import load_dotenv
from agent.tools import search_places, get_weather, get_flight_status, search_hotels

load_dotenv()

async def debug_tools():
    print("--- TESTING TOOLS ---")
    
    # Test Hotels
    print("\n1. Testing Hotels (Munnar)...")
    try:
        res = await search_hotels.ainvoke({"city": "Munnar"})
        print(f"Result: {res[:200]}..." if len(res) > 200 else res)
    except Exception as e:
        print(f"ERROR: {e}")

    # Test Flights
    # assuming we have a valid key, let's test a common route
    print("\n2. Testing Flights (DEL to BOM)...")
    try:
        res = await get_flight_status.ainvoke({"departure": "DEL", "arrival": "BOM"})
        print(f"Result: {res}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(debug_tools())

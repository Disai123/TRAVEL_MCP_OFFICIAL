import asyncio
import os
from dotenv import load_dotenv
from agent.graph import app
from langchain_core.messages import HumanMessage

load_dotenv()

async def debug_run():
    print("Testing Agent Invocation...")
    try:
        inputs = {
            "messages": [HumanMessage(content="Hello, check weather in Paris")],
            "source": "London",
            "destination": "Paris"
        }
        print("Invoking graph...")
        result = await app.ainvoke(inputs)
        print("Success!")
        print(result)
    except Exception as e:
        print("\nCRASH DETECTED:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_run())

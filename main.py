from fastapi import FastAPI
import asyncio

app = FastAPI()

async def background_task(message: str):
    # Simulate a background task (e.g., processing data)
    await asyncio.sleep(5)
    print(f"Background task: {message}")

@app.post("/process-data")
async def process_data():
    # Process the main request
    result = {"message": "Data processing started"}

    # Trigger the background task
    asyncio.create_task(background_task("Data processing in the background"))

    return result

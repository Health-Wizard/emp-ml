from fastapi import FastAPI, BackgroundTasks, Depends
from prisma import Prisma

app = FastAPI()

def get_db():
    db = Prisma()
    try:
        yield db
    finally:
        db.disconnect()
        

async def fetch_data(db: Prisma):
    print("Fetching data from the database...")
    # Replace this with your actual Prisma query to fetch data
    await db.connect()
    data = await db.employee.find_many()
    data = await db.employee.find_many()
    data = await db.employee.find_many()
    data = await db.employee.find_many()
    print(data)
    for i in range(1000000):
        print(i)
    db.disconnect()
    return data

async def process_data(data):
    print("Processing data...")
    # Replace this with your actual data processing logic
    return data

@app.get("/")
async def root():
    return {"statuc" : "running"}

@app.get("/fetch", status_code=200)
async def fetch_and_process_data(background_tasks: BackgroundTasks, db: Prisma = Depends(get_db)):
    # Fetch data in the background
    background_tasks.add_task(fetch_and_process_data_background, db)
    return {"message": "Fetching and processing data in the background."}

async def fetch_and_process_data_background(db: Prisma):
    data = await fetch_data(db)
    processed_data = await process_data(data)
    # You can store or use the processed_data as needed

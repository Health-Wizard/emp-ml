from fastapi import FastAPI, BackgroundTasks
from app.slack_utlis import fetch_conversations
from app.metrics_utils import calculate_health_index
from app.schema import ResponseData
from app.db import Session
from app.models import Channels,Employee
import logging

# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)
app = FastAPI()

status = None


# save in bulk to db
def save_to_db(db, data):
    db.bulk_save_objects(data)
    db.commit()


# start of the processing of the data
def process_data():
    logging.info("Processing started")
    try:
        db = Session()
        # channels = db.query(Channels).all()
        emp_details = db.query(Employee.empId,Employee.companyEmail, Employee.role, Employee.department).all()
        messages,channels_details = fetch_conversations()
        messages= []
        health_data = calculate_health_index(messages,emp_details)
        # channels_details = [Channels(**channel) for channel in channels_details]
        # print(channels_details)
        # save_to_db(db,channels_details)
        save_to_db(db,health_data)
        # db.bulk_save_objects(health_data)
        # db.commit()
    except Exception as err:
        logging.error(err)
        db.rollback()
    finally:
        
        db.close()



@app.get("/")
def root():
    return {"message": "Server running"}


@app.get("/trigger-metric", response_model=ResponseData, status_code=200)
async def trigger_employee_data(background_tasks: BackgroundTasks):
    global status
    if status == None:
        status = "running"
        background_tasks.add_task(process_data)
    return ResponseData(
        status=status,
        data=[]
    )
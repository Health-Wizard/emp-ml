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


# def map_emp_to_dict(emp_details):
#     employees = {}
#     for emp in emp_details:
#         {
#             'empId': 
#         }

def process_data():
    # store message data
    logging.info("Processing started")
    try:
        db = Session()
        # channels = db.query(Channels).all()
        emp_details = db.query(Employee.empId,Employee.companyEmail, Employee.role, Employee.department).all()
        # print(employee_data)
        messages,channels_details = fetch_conversations()
        health_data = calculate_health_index(messages,emp_details)
        # channels_details = [Channels(**channel) for channel in channels_details]
        # print(channels_details)
        db.bulk_save_objects(health_data)
        db.commit()
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
    # await fetch_from_db()
    process_data()
    # background_tasks.add_task(process_data)
    return ResponseData(
        status=status,
        data=[]
    )
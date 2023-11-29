from fastapi import FastAPI, BackgroundTasks
from app.slack_utlis import fetch_conversations
from app.metrics_utils import calculate_health_index
from app.schema import EmployeeHealthAnalysis, ResponseData, TimeFrame
from app.constant import SENTIMENT_LABELS
import logging
import datetime
from prisma import Prisma

# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)

health_data = []

status = None
emp_details = None
channel_details = None

# async def fetch_from_db():
#     global emp_details
#     db = Prisma()
#     await db.connect()
#     channel_details = await db.channels.find_many()
#     emp_list = await db.employee.find_many()
#     print(channel_details)
#     employee_details = pd.DataFrame([vars(emp) for emp in emp_list])
#     employee_details.drop(columns=['id', 'username', 'name', 'companyEmail'],inplace=True)
#     employee_details['empId'] = employee_details['empId'].astype(int)
#     employee_details.set_index('empId', inplace=True)
#     employee_details['happiness_index'] = 0.0
#     employee_details['stree_label'] = 0.0
#     employee_details['sentiment'] = SENTIMENT_LABELS[2]
#     emp_details = employee_details
#     await db.disconnect()

def process_data():
    global health_data, status
    # store message data
    logging.info("Processing started")
    messages = fetch_conversations()
    
    return calculate_health_index(messages)

    # messages_details = pd.DataFrame.from_dict(messages)
    # msg_groupby_user = messages_details.groupby('user_id')

    # for user_id, msges_data in msg_groupby_user:
    #     health_metrics = calculate_health_index(int(user_id), msges_data, emp_details)
    #     health_data.append(EmployeeHealthAnalysis(
    #         user_id=user_id,
    #         period= TimeFrame(startDate=startDate.isoformat(), endDate=endDate.isoformat()),
    #         health_metrics=health_metrics
    #     ))
    
    # status = "completed"


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Server running"}


@app.get("/trigger-metric", response_model=ResponseData, status_code=200)
async def trigger_employee_data(background_tasks: BackgroundTasks):
    global status
    if status == None:
        status = "running"
    # await fetch_from_db()
    health_data = process_data()
    # background_tasks.add_task(process_data)
    return ResponseData(
        status=status,
        data=health_data
    )
@app.get("/metric", response_model=ResponseData, status_code=200)
def get_employee_data():
    global status
    response = None
    if status == "running":
        return ResponseData(
            status=status,
            data=[]
        )
    
    if status == "Error":
        return
    response = ResponseData(
        status=status,
        data=health_data
    )
    status = None
    return response
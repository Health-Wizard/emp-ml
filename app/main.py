from fastapi import FastAPI, BackgroundTasks
from app.text_util import fetch_channels, fetch_messages
from app.metrics_utils import calculate_health_index
from app.schema import EmployeeHealthAnalysis, ResponseData
import pandas as pd
import logging
import time

# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)
health_data = []
status = None


def process_data():
    global health_data, status

    # store message data
    messages = []

    # fetch channel link from the db
    channel_details = fetch_channels()

    if not channel_details:
        logging.info("No channels found!!!!")
        status = "Error"
        return

    logging.info(f"Channels fetched :{str(len(channel_details))}")

    # fetch channel related messages and employee details from sendbird
    for channel in channel_details:
        msges_data = fetch_messages(channel['url'],channel['name'], channel['last_message_id'])
        logging.info(f"Messages fetch from channel: {channel['name']}")
        if len(msges_data) == 0:
            continue
        messages.extend(msges_data)
        break
    msg_data = pd.DataFrame.from_dict(messages)
    msg_groupby_user = msg_data.groupby('user_id')
    for user_id, msges_data in msg_groupby_user:
        health_metrics = calculate_health_index(msges_data)
        health_data.append(EmployeeHealthAnalysis(
            user_id=user_id,
            health_metrics=health_metrics
        ))

    status = "completed"


app = FastAPI()


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


@app.get("/metric", response_model=ResponseData, status_code=200)
async def get_employee_data():
    global status
    response = None
    if status == "running":
        return ResponseData(
            status=status,
            data=[]
        )
    
    if status == "Error":
        return
    print(health_data) 
    response = ResponseData(
        status=status,
        data=health_data
    )
    status = None
    return response
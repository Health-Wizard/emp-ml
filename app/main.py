from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.util import remove_punctuation_numbers_special_chars
from typing import List
from app.constant import EMOTION_MODEL, DEPRESSION_MODEL
from app.model import Model
from app.db import EmployeeMesaage, EmployeeDetails, HealthData
import app.schema as schema
from datetime import datetime, timedelta

# emotion_classifier = Model(EMOTION_MODEL).get_pipeline()
# depression_classifier = Model(DEPRESSION_MODEL).get_pipeline()



def get_prediction(pipeline, text: str):
    return pipeline(text)[0]['label']


def calculate_rate(ecurr: int, etotal: int, dcurr: int) -> float:
    return round((ecurr + dcurr)/(etotal)*10, 1)


# def predict_class(text: str):
#     global emotion_classifier, depression_classifier
#     filtered_text = remove_punctuation_numbers_special_chars(text)
#     emotion = get_prediction(emotion_classifier, filtered_text)
#     depressed = ""
#     if emotion not in HAPPY_LABEL:
#         depressed = get_prediction(depression_classifier, filtered_text)
#     row['depressed'] = True if depressed == 'LABEL_1' else False
#     row['emotion'] = emotion
#     return row

def get_data(connection, query={}, filter={}, limit=0, skip=0):
    data = connection.find(query, filter).skip(
        skip).limit(limit)
    return data


def process_data():
    emp_emails = get_data(connection=EmployeeDetails,
                          filter={'email': 1, '_id': 0})
    print(emp_emails)
    print(EmployeeDetails.find())
    end_date = (datetime(2023, 3, 22, 23, 37, 18)).replace(
        hour=10, minute=0, second=0)
    start_date = end_date - timedelta(weeks=1)
    # for email in emp_emails:
    #     query = {"user_id": email, "date_time": {"$gte": start_date, "$lte": end_date}}
    #     user_msgs = mongo_data.get_data(query=query, filter={'text':1, '_id': 0}, collection_name=EMPLOYEE_MESSAGES_COLLECTION,index='user_id')
    # # Get data from the collection
    # }
    # # df = mongo_data.get_data(
    # #     query=query)
    # df = df.groupby('user_id').apply(predict_class, axis=1)
    # return df.to_dict(orient='records')


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Server running"}
# , response_model=schema.EmployeeHealthAnalysis


@app.get("/data")
async def process_employee_data():
    # background_tasks.add_task(process_data)
    process_data()
    return {"success": "done"}

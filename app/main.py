from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.util import remove_punctuation_numbers_special_chars
from app.constant import EMOTION_MODEL, DEPRESSION_MODEL, LABEL_SCORES, STRESS_LABELS
from app.model import Model
from app.db import EmployeeMesaage, EmployeeDetails, HealthData
import app.schema as schema
from datetime import datetime, timedelta
import pandas as pd
from typing import List
import logging
from collections import Counter


# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)

emotion_classifier = Model(EMOTION_MODEL).get_pipeline()
depression_classifier = Model(DEPRESSION_MODEL).get_pipeline()

data = pd.DataFrame()


def get_prediction(pipeline, text: str):
    return pipeline(text)[0]['label']


def calculate_rate(ecurr: int, etotal: int, dcurr: int) -> float:
    return round((ecurr + dcurr)/(etotal)*10, 1)


def predict_class(row):
    global emotion_classifier, depression_classifier
    filtered_text = remove_punctuation_numbers_special_chars(row['text'])
    logging.info("Text filtered..")
    emotion = get_prediction(emotion_classifier, filtered_text)
    depressed = get_prediction(depression_classifier, filtered_text)
    row['depressed'] = True if depressed == 'LABEL_1' else False
    row['emotion'] = emotion
    logging.info("Text predicted..")
    return row


def calculate_health_index(emotions: list[str], depression: list[bool]):
    total_score = sum(LABEL_SCORES[emotion] for emotion in emotions)
    possitivity_rate = (total_score/(len(emotions)*10))
    stress_from_emotions = sum(
        STRESS_LABELS[emotion] for emotion in emotions) / (len(emotions) * 10)
    stress_from_depression = sum(5 if value else 0 for value in depression) / (
        len(depression) * 5)   # Higher stress if depressed
    # Higher stress for lower positivity rate
    stress_from_positivity = (1 - possitivity_rate)
    # Combine the stress factors with weights (you can adjust the weights based on importance)
    stress_level = 0.6 * stress_from_emotions + \
        0.3 * stress_from_depression + 0.1 * stress_from_positivity
    health_data = [schema.AnalyticsData(
        title="Happiness Level of Employee",
        data=[possitivity_rate],
        range=[0, 1],
        graph_type="progress bar"
    ),
        schema.AnalyticsData(
        title="Stress Level of Employee",
        data=[stress_level],
        range=[0, 1],
        graph_type="progress bar"
    ),
        schema.AnalyticsData(
        title="Mood Graph of Employee",
        data=[dict(Counter(emotions))],
        graph_type="pie graph"
    )
    ]
    return health_data


def get_data(connection, query={}, filter={}, limit=0, skip=0):
    data = connection.find(query, filter).skip(
        skip).limit(limit)
    return data


def process_data():
    emp_data = get_data(connection=EmployeeDetails,
                        filter={'email': 1, '_id': 0})
    logging.info("Emails fetched.")
    user_emails = [email['email'] for email in emp_data]
    end_date = (datetime(2023, 3, 22, 23, 37, 18)).replace(
        hour=10, minute=0, second=0)
    start_date = end_date - timedelta(weeks=1)
    health_data = []
    for email in user_emails[:2]:
        query = {"user_id": email, "date_time": {
            "$gte": start_date, "$lte": end_date}}
        emp_msgs = get_data(connection=EmployeeMesaage,
                            query=query, filter={'text': 1, '_id': 0})
        logging.info("Messages fetched!!")

        df_texts = pd.DataFrame(emp_msgs)
        df_texts = df_texts.apply(predict_class, axis=1)
        logging.info("Emotions and depression predicted!!!")

        health_metrics = calculate_health_index(
            df_texts['emotion'].tolist(), df_texts['depressed'].tolist())
        logging.info("Index Calculated")
        health_data.append(schema.EmployeeHealthAnalysis(
            user_id=email,
            period=schema.TimeFrame(
                startDate=start_date,
                endDate=end_date
            ),
            health_metrics=health_metrics
        ))
    return health_data


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Server running"}


@app.get("/data", response_model=List[schema.EmployeeHealthAnalysis])
async def process_employee_data():
    # background_tasks.add_task(process_data)
    return process_data()

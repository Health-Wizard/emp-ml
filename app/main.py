from fastapi import FastAPI,BackgroundTasks
from fastapi.responses import JSONResponse
from app.util import remove_punctuation_numbers_special_chars
import app.constant as constant
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

classifier = Model(constant.CLASSIFICATION_MODEL).get_pipeline()

data = pd.DataFrame()


def get_prediction(text: str, label: list[str]):
    return classifier(text, label, multi_label=False)


def get_predicted_label(text: str, labels: list[str]):
    emotions = get_prediction(text=text, label=labels)
    em_labels = emotions['labels']
    scores = emotions['scores']
    max_score = max(scores)
    ind = scores.index(max_score)
    label = em_labels[ind]
    return label


def predict_emotions(row):
    filtered_text = remove_punctuation_numbers_special_chars(row['text'])
    logging.info("Text filtered..")
    emotion_label = get_predicted_label(
        text=filtered_text, labels=constant.EMOTION_LABEL)
    label = ""
    if emotion_label == 'sadness':
        label = get_predicted_label(filtered_text, constant.SAD_LABEL)
        logging.info("Sadness label predicted..")
    elif emotion_label == 'happiness':
        label = get_predicted_label(filtered_text, constant.HAPPY_LABEL)
        logging.info("Happiness label predicted..")
    elif emotion_label == 'disgust':
        label = get_predicted_label(filtered_text, constant.DISGRUST_LABEL)
        logging.info("Digust label predicted..")
    elif emotion_label == 'anger':
        label = get_predicted_label(filtered_text, constant.ANGER_LABEL)
        logging.info("Anger label predicted..")
    elif emotion_label == 'fear':
        label = get_predicted_label(filtered_text, constant.FEAR_LABEL)
        logging.info("Fear label predicted..")
    elif emotion_label == 'surprise':
        label = get_predicted_label(filtered_text, constant.SURPRISE_LABEL)
        logging.info("Surprise label predicted..")
    else:
        label = get_predicted_label(filtered_text, constant.NEUTRAL_LABEL)
        logging.info("Neutral label predicted..")
    row['emotion'] = label
    return row


def calculate_health_index(emotions: list[str]):
    positive_score = 0
    stress_score = 0
    depress_score = 0
    total_score = len(emotion)
    depressions = constant.ANGER_LABEL + constant.DISGRUST_LABEL + \
        constant.FEAR_LABEL + constant.SAD_LABEL
    for emotion in emotions:
        positive_score = positive_score + constant.LABEL_SCORES[emotion]
        stress_score = stress_score + (10 - constant.LABEL_SCORES[emotion])
        if emotion in depressions:
            depress_score = depress_score + 5

    possitivity_rate = (positive_score/(total_score*10))
    stress_from_emotions = stress_score / (total_score * 10)

    stress_from_depression = depress_score / (total_score * 5)
    stress_level = 0.6 * stress_from_emotions + 0.3 * stress_from_depression
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




async def process_data():

    # fetch channel link from the db

    # fetch employee details from db

    # fetch channel related messages from db
    emp_data = get_data(connection=EmployeeDetails,
                        filter={'email': 1, '_id': 0})
    logging.info("Emails fetched.")
    user_emails = [email['email'] for email in emp_data]
    end_date = (datetime(2023, 3, 22, 23, 37, 18)).replace(
        hour=10, minute=0, second=0)
    start_date = end_date - timedelta(weeks=1)
    health_data = []
    for email in user_emails[:1]:
        query = {"user_id": email, "date_time": {
            "$gte": start_date, "$lte": end_date}}
        emp_msgs = get_data(connection=EmployeeMesaage,
                            query=query, filter={'text': 1, '_id': 0})
        logging.info("Messages fetched!!")

        df_texts = pd.DataFrame(emp_msgs)
        df_texts = df_texts.apply(predict_emotions, axis=1)
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


@app.get("/analytics")
async def process_employee_data(background_tasks: BackgroundTasks):
    response = {"status": "running"}
    background_tasks.add_task(process_data)
    # response["data"] = heathData
    return response

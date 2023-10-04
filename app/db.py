from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi
import pandas as pd
from app.constant import DB_URL, DB_NAME
from pymongo.errors import PyMongoError
import logging


# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)


def connect():
    try:
        client = MongoClient(DB_URL, server_api=ServerApi('1'))
        logging.info("success fully connected to mongodb...")
    except PyMongoError as e:
        print(e)
    return client


def connect_db(client):
    db = client[DB_NAME]
    return db


def close_connection(client):
    try:
        client.close()
        logging.info("Successfully closed client")
    except PyMongoError as e:
        logging.error(repr(e))


client = connect()
db = connect_db(client=client)
EmployeeDetails = db['employee_details']
EmployeeDetails.create_index('email', unique=True)
EmployeeMesaage = db['employee_messages']
EmployeeMesaage.create_index('user_id')
HealthData = db['employee_health_analytics']
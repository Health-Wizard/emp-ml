from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi
import pandas as pd
from app.constant import DB_URL, DB_NAME
from pymongo.errors import PyMongoError
import logging


# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)


class EmployeeDB:
    def __init__(self):
        self.uri = DB_URL
        self.db_name = DB_NAME
        self.client = self.connect()
        self.db = self.connect_db()

    def connect(self):
        try:
            client = MongoClient(self.uri, server_api=ServerApi('1'))
            logging.info("success fully connected to mongodb...")
        except PyMongoError as e:
            print(e)
        return client

    def connect_db(self):
        db = self.client[self.db_name]
        return db

    def connect_collection(self, collection_name, index=None):
        collection = self.db[collection_name]
        if not index:
            collection.create_index((index, ASCENDING), name=index)
        return collection

    def close_connection(self):
        try:
            self.client.close()
            logging.info("Successfully closed client")
        except PyMongoError as e:
            logging.error(repr(e))


empDB = EmployeeDB()
EmployeeDetails = empDB.db['employee_details']
EmployeeMesaage = empDB.db['employee_messages']
HealthData = empDB.db['employee_health_analytics']

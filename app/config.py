import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.DRIVERNAME = os.getenv("DRIVERNAME")
        self.USERNAME= os.getenv("DB_USER")
        self.PASSWORD = os.getenv("PASSWORD")
        self.HOST = os.getenv("HOST")
        self.DATABASE = os.getenv("DATABASE")
        self.PORT = os.getenv('PORT')
        self.TOKEN = os.getenv('TOKEN')

# Create an instance of Config
env_config = Config()
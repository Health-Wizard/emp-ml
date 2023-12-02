from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

url = URL.create(
    drivername="postgresql",
    username="admin",
    password="XHCqU8BUdK1vW7UHqdgaMC5NsaJhgvVg",
    host="dpg-ckvujf237rbc73f3lan0-a.singapore-postgres.render.com",
    database="employee_nb07",
    port=5432
)

engine = create_engine(url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
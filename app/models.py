from sqlalchemy import Column, Integer, String, Float, DateTime,JSON,ForeignKey
from sqlalchemy.orm import declarative_base,relationship
from app.db import engine

Base = declarative_base()

class Channels(Base):
    __tablename__ = "Channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=True)
    channel_id = Column(String, unique=True, nullable=False)
    created_timestamp = Column(Float, nullable=False)
    last_message_id = Column(String, nullable=True, default="")


class Employee(Base):
    __tablename__ = "Employee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    empId = Column(Integer, unique=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    companyEmail = Column(String, nullable=False, unique=True)
    designation = Column(String, nullable=False, unique=False)
    department = Column(String, nullable=True, unique=False)
    dateOfJoining = Column(DateTime, nullable=False, unique=False)
    salary = Column(String, nullable=True, unique=False)
    role = Column(String, nullable=False, unique=True)
    gender = Column(String, nullable=True, unique=False)
    age = Column(Integer, nullable=True, unique=False)

class HealthData(Base):
    __tablename__ = "Health_Analytics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    empId = Column(Integer,ForeignKey('Employee.empId'), unique=True)
    startDate = Column(DateTime, nullable=False, unique=False)
    endDate = Column(DateTime, nullable=False, unique=False)
    health_data = Column(JSON,)

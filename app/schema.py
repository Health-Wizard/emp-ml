from pydantic import BaseModel
from typing import List
from datetime import datetime


class EmployeeDetails(BaseModel):
    _id: str
    email: str
    age: str
    sex: str


class AnalyticsData(BaseModel):
    title: str
    data: list[float]
    graph_type: str


class TimeFrame(BaseModel):
    startDate: datetime
    endDate: datetime


class EmployeeMessage(BaseModel):
    text: str
    user_id: str
    date_time: str


class EmployeeHealthAnalysis(BaseModel):
    user_id: str
    period: TimeFrame
    health_data: List[AnalyticsData]

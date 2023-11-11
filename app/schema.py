from pydantic import BaseModel
from typing import List
from datetime import datetime


class EmployeeDetails(BaseModel):
    _id: str = None
    email: str = None
    age: str = None
    sex: str = None


class AnalyticsData(BaseModel):
    title: str
    data: list
    range: list[int] | None = None
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
    # period: TimeFrame
    health_metrics: List[AnalyticsData]

class ResponseData(BaseModel):
    status:str
    data : List[EmployeeHealthAnalysis]  = None

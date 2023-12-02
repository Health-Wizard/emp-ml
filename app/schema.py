from pydantic import BaseModel
from typing import List
from datetime import datetime


class EmployeeDetails(BaseModel):
    _id: str = None
    email: str = None
    age: str = None
    sex: str = None

class AnalyticsData(BaseModel):
    title: str = None
    data: list = None
    range: list | None = None
    label: list = None
    xrange: list = None
    graph_type: str = None


class TimeFrame(BaseModel):
    startDate: datetime
    endDate: datetime

class Channels(BaseModel):
    url : str
    name: str
    create_timestamp : str
    member_count: int
    type: str
    last_message_id : int

class EmployeeMessage(BaseModel):
    text: str
    user_id: str
    date_time: str

class EmployeeHealthAnalysis(BaseModel):
    user_id: int
    period: TimeFrame
    health_metrics: List[AnalyticsData] = None

class ResponseData(BaseModel):
    status:str
    data : List[EmployeeHealthAnalysis]  = None
    channel : List[Channels] = None

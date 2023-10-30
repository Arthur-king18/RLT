from datetime import datetime
from typing import List

from pydantic import BaseModel

class GetRequestMessage(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: str


class GetData(BaseModel):
    dataset: List[int] | None
    labels: List[datetime] | None


class DateAndTotalValue(BaseModel):
    _id: datetime
    total_value: int


class GetDataFromDataBase(BaseModel):
    data: List[DateAndTotalValue]
from pydantic import BaseModel
from typing import List
from app.models.sensor import SensorReading

class SensorHistoryResponse(BaseModel):
    readings: List[SensorReading]
    total: int
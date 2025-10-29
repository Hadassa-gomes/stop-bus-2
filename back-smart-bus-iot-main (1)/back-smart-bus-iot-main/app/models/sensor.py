from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorReadingCreate(BaseModel):
    temperature: float = Field(..., ge=-40.0, le=80.0)
    humidity: float = Field(..., ge=0.0, le=100.0)
    device_id: Optional[str] = None

class SensorReading(SensorReadingCreate):
    id: str
    recorded_at: datetime
    heat_index: Optional[float] = None
    
    class Config:
        from_attributes = True
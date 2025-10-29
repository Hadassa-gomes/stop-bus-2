from typing import Dict, Any
from app.utils.cleaning import clean_reading
from app.crud.sensors import create_reading, get_latest_reading, get_history, get_total_readings
from app.core.database import get_db
from app.core.config import settings
import math

class SensorService:
    def __init__(self):
        self.collection_name = settings.mongodb_collection
    
    async def process_and_store(self, raw_data: Dict[str, Any]) -> str:
        # 1. Limpeza e validação
        cleaned = clean_reading(
            raw_data.get("temperature"),
            raw_data.get("humidity")
        )
        
        # 2. Cálculo Heat Index
        heat_index = self._calculate_heat_index(cleaned["temperature"], cleaned["humidity"])
        
        # 3. Documento final
        doc = {
            **cleaned,
            "device_id": raw_data.get("device_id"),
            "heat_index": heat_index,
            "raw": raw_data
        }
        
        # 4. Persistir
        db = await anext(get_db())
        return await create_reading(db[self.collection_name], doc)
    
    async def get_latest(self) -> Dict[str, Any]:
        db = await anext(get_db())
        return await get_latest_reading(db[self.collection_name])
    
    async def get_history_data(self, limit: int = 100) -> Dict[str, Any]:
        db = await anext(get_db())
        readings = await get_history(db[self.collection_name], limit)
        total = await get_total_readings(db[self.collection_name])
        return {"readings": readings, "total": total}
    
    def _calculate_heat_index(self, temp: float, hum: float) -> float:
        """NOAA Heat Index Formula"""
        if hum < 13 and temp >= 80:
            hi = (-42.379 + 2.04901523*temp + 10.14333127*hum -
                  0.22475541*temp*hum - 0.00683783*temp*temp -
                  0.05481717*hum*hum + 0.00122874*temp*temp*hum +
                  0.00085282*temp*hum*hum - 0.00000199*temp*temp*hum*hum)
            adjustment = ((13 - hum) / 4) * math.sqrt((17 - abs(temp - 95.)) / 17)
            hi += adjustment
        else:
            hi = temp
        return round(hi, 2)
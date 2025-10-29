import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ThingspeakService:
    def __init__(self):
        self.url = "http://api.thingspeak.com/update"
        self.api_key = settings.thingspeak_write_api_key
    
    async def send_data(self, temperature: float, humidity: float) -> bool:
        """Envia dados para Thingspeak"""
        try:
            params = {
                "api_key": self.api_key,
                "field1": temperature,
                "field2": humidity
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.url, params=params)
                
            success = response.status_code == 200
            if success:
                logger.info(f"✅ Thingspeak: T={temperature}°C H={humidity}%")
            else:
                logger.error(f"❌ Thingspeak: {response.status_code}")
                
            return success
            
        except Exception as e:
            logger.error(f"❌ Thingspeak Error: {e}")
            return False
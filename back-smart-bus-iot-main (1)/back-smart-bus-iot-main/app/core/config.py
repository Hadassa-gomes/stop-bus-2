from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str
    mongodb_db: str = "smart_bus_stop"
    mongodb_collection: str = "sensor_readings"
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Thingspeak
    thingspeak_write_api_key: str
    
    # IoT
    iot_api_key: str
    
    # CORS
    allowed_origins_str: str = "http://localhost:3000"
    
    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_str.split(",")]
    
    class Config:
        env_file = ".env"

settings = Settings()
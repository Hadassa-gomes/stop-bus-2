from fastapi import APIRouter, Depends, HTTPException, Header, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.models.sensor import SensorReading
from app.services.thingspeak_service import ThingspeakService
import logging

router = APIRouter(prefix="/api/v1/sensors", tags=["Sensors"])
logger = logging.getLogger(__name__)

# Instância global do serviço ThingSpeak
thingspeak_service = ThingspeakService()


# 🚀 Endpoint principal de ingestão de dados (vindo do ESP32)
@router.post("/ingest")
async def ingest_data(
    reading: SensorReading,
    db: AsyncIOMotorDatabase = Depends(get_db),
    x_api_key: str = Header(None)
):
    """Recebe dados do sensor, salva no MongoDB e envia ao ThingSpeak."""
    from app.core.config import settings

    if x_api_key != settings.iot_api_key:
        raise HTTPException(status_code=401, detail="Chave IoT inválida.")

    try:
        result = await db.sensor_readings.insert_one(reading.dict())
        logger.info(f"📥 Sensor data saved: {result.inserted_id}")

        await thingspeak_service.send_data(
            temperature=reading.temperature,
            humidity=reading.humidity
        )
        logger.info("✅ Dados enviados ao ThingSpeak com sucesso.")

        return {"status": "ok", "id": str(result.inserted_id)}

    except Exception as e:
        logger.error(f"❌ Erro ao processar dados do sensor: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 🧪 Endpoint de teste manual do ThingSpeak
@router.get("/test_thingspeak")
async def test_thingspeak(
    temperature: float = Query(..., description="Temperatura de teste"),
    humidity: float = Query(..., description="Umidade de teste")
):
    """Envia manualmente uma leitura ao ThingSpeak para teste."""
    try:
        success = await thingspeak_service.send_data(temperature, humidity)
        if success:
            return {
                "status": "success",
                "message": f"Dados enviados ao ThingSpeak: {temperature}°C / {humidity}%",
            }
        else:
            raise HTTPException(status_code=400, detail="Falha ao enviar ao ThingSpeak.")
    except Exception as e:
        logger.error(f"❌ Erro no teste do ThingSpeak: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Última leitura salva no banco (para o dashboard)
@router.get("/latest")
async def get_latest_reading(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Retorna a leitura mais recente do sensor.
    Exemplo de resposta:
    {
        "temperatura": 25.6,
        "umidade": 80,
        "onibus": ["Bus 101", "Bus 202"]
    }
    """
    try:
        doc = await db.sensor_readings.find_one(sort=[("_id", -1)])  # Busca o último documento
        if not doc:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")

        # Ajuste o nome das chaves conforme o que o seu banco realmente salva
        temperatura = doc.get("temperature", 0)
        umidade = doc.get("humidity", 0)

        # Por enquanto, vamos simular a lista de ônibus na parada:
        onibus = ["Bus 101", "Bus 202"]  # depois pode conectar com outro serviço

        return {
            "temperatura": temperatura,
            "umidade": umidade,
            "onibus": onibus
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar última leitura: {e}")

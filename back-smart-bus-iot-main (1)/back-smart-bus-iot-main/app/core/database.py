from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Cliente global (será inicializado na primeira chamada)
_sync_client = None

async def get_motor_client():
    """Retorna cliente Motor async com ServerApi"""
    return AsyncIOMotorClient(settings.mongodb_url, server_api=ServerApi('1'))

async def get_db():
    """Context manager para database"""
    client = await get_motor_client()
    try:
        yield client[settings.mongodb_db]
    finally:
        client.close()

def init_db():
    """Inicializa DB e cria índices"""
    global _sync_client
    try:
        logger.info("🔍 Conectando ao MongoDB Atlas...")
        _sync_client = MongoClient(settings.mongodb_url, server_api=ServerApi('1'))
        
        # Confirmar conexão
        _sync_client.admin.command('ping')
        logger.info("✅ Pinged your deployment. You successfully connected to MongoDB!")
        
        db = _sync_client[settings.mongodb_db]
        collection = db[settings.mongodb_collection]
        
        # Índices otimizados
        collection.create_index("recorded_at", background=True)
        collection.create_index([("device_id", 1), ("recorded_at", -1)], background=True)
        
        logger.info("✅ MongoDB conectado e índices criados!")
        logger.info(f"📊 Database: {settings.mongodb_db}")
        logger.info(f"📁 Collection: {settings.mongodb_collection}")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar MongoDB: {e}")
        logger.warning("⚠️ Continuando sem MongoDB...")
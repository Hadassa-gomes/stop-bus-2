from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime

async def create_reading(collection: AsyncIOMotorCollection, reading: Dict[str, Any]) -> str:
    reading["recorded_at"] = datetime.utcnow()
    result = await collection.insert_one(reading)
    return str(result.inserted_id)

async def get_latest_reading(collection: AsyncIOMotorCollection) -> Dict[str, Any]:
    return await collection.find_one({}, sort=[("recorded_at", -1)])

async def get_history(collection: AsyncIOMotorCollection, limit: int = 100) -> List[Dict[str, Any]]:
    cursor = collection.find().sort("recorded_at", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def get_total_readings(collection: AsyncIOMotorCollection) -> int:
    """Retorna total de leituras"""
    return await collection.count_documents({})

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.user import UserInDB, UserCreate
from app.core.security import get_password_hash, verify_password

async def create_user(collection: AsyncIOMotorCollection, user: UserCreate) -> str:
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed_password,
        "is_active": True
    }
    result = await collection.insert_one(user_doc)
    return str(result.inserted_id)

async def get_user_by_email(collection: AsyncIOMotorCollection, email: str) -> Optional[dict]:
    return await collection.find_one({"email": email})

async def authenticate_user(collection: AsyncIOMotorCollection, email: str, password: str) -> Optional[dict]:
    user = await get_user_by_email(collection, email)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

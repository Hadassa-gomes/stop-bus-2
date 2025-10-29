from fastapi import HTTPException, status
from datetime import timedelta
from app.core.security import create_access_token
from app.crud.user import authenticate_user, create_user
from app.core.database import get_db
from app.models.user import UserInDB
from app.core.config import settings

async def login(email: str, password: str):
    db = await anext(get_db())
    user = await authenticate_user(db["users"], email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

async def register(user_data: UserInDB):
    db = await anext(get_db())
    existing = await db["users"].find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = await create_user(db["users"], user_data)
    return {"user_id": user_id, "message": "User created successfully"}
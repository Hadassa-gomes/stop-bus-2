from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import Token, UserCreate, UserLogin
from app.crud.users import create_user, authenticate_user
from app.core.database import get_db
from app.core.security import create_access_token
import motor.motor_asyncio

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)):
    """Registra novo usuário"""
    db_user = await db["users"].find_one({"email": user.email})
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_id = await create_user(db["users"], user)
    return {"msg": "User created", "user_id": user_id}

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)):
    """Login do usuário"""
    user = await authenticate_user(db["users"], user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"sub": user["email"]}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

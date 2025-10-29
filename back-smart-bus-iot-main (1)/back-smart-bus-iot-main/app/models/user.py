from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[str] = None  # Opcional para criação
    hashed_password: str
    is_active: bool = True
    
    class Config:
        from_attributes = True
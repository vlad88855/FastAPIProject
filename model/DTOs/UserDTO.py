from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from model.UserORM import UserRole

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(description="User email")
    password: str = Field(min_length=6, max_length=128, description="User password")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    avatar_url: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    avatar_url: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
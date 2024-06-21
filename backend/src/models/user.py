from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: constr(min_length=10, max_length=15)
    user_type: str
    password: str
    address: str

class User(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    phone: constr(min_length=10, max_length=15)
    user_type: str
    address: str
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(min_length=10, max_length=15)] = None
    address: Optional[str] = None
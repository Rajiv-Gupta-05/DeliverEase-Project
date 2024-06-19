from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    phone: str
    user_type: str
    address: str
    password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
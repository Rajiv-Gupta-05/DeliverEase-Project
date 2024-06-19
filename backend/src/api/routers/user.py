from fastapi import APIRouter, HTTPException
from typing import List
from src.api.models.user import User
from src.api.crud.user import get_users

router = APIRouter()

@router.get("/users", response_model=List[User])
async def read_users():
    users = await get_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users
import asyncpg
from fastapi import APIRouter, HTTPException
from typing import List
from src.models.user import UserCreate, User
from src.api.dao.user import get_users, create_user

router = APIRouter()

@router.get("/users", response_model=List[User])
async def read_users():
    users = await get_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.post("/register", response_model=User)
async def register_user(user: UserCreate):
    try:
        new_user = await create_user(user)
        return new_user
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User with this email or phone already exists")
import asyncpg
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.models.user import UserCreate, User, UserUpdate
from src.api.dao.user import get_users, create_user, update_user
from src.api.dependencies import get_current_user

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
    
@router.put("/updateprofile", response_model=User)
async def update_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    try:
        updated_user = await update_user(current_user.user_id, user_update)
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
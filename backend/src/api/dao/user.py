import asyncpg
import logging
import bcrypt
from typing import List, Optional
from src.models.user import UserCreate, User, UserUpdate
from src.models.db.database import database
from datetime import datetime
from fastapi import HTTPException

logger = logging.getLogger(__name__)

async def get_users() -> List[User]:
    query = "SELECT name, email, phone, password, user_type, address, created_at, updated_at from users"
    rows = await database.connection.fetch(query)
    return [User(**dict(row)) for row in rows]

async def create_user(user: UserCreate) -> User:
    query = """
        INSERT INTO users (name, email, phone, user_type, password, address, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING user_id, name, email, phone, user_type, address, created_at, updated_at
    """
    created_at = updated_at = datetime.utcnow()

    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    row = await database.connection.fetchrow(query, user.name, user.email, user.phone, user.user_type, hashed_password, user.address, created_at, updated_at)
    return User(**dict(row))

async def get_user_by_id(user_id: int) -> Optional[User]:
    query = "SELECT user_id, name, email, phone, user_type, address, created_at, updated_at FROM users WHERE user_id = $1"
    row = await database.connection.fetchrow(query, user_id)
    if row:
        return User(**dict(row))
    return None

async def update_user(user_id: int, user_update: UserUpdate) -> Optional[User]:
    logger.debug(f"Updating user_id {user_id} with data {user_update.dict()}")
    query = """
        UPDATE users
        SET name = COALESCE($2, name),
            email = COALESCE($3, email),
            phone = COALESCE($4, phone),
            address = COALESCE($5, address),
            updated_at = $6
        WHERE user_id = $1
        RETURNING user_id, name, email, phone, user_type, address, created_at, updated_at
    """
    updated_at = datetime.utcnow()
    row = await database.connection.fetchrow(query, user_id, user_update.name, user_update.email, user_update.phone, user_update.address, updated_at)
    if row:
        return User(**dict(row))
    else:
        logger.error(f"User with user_id {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
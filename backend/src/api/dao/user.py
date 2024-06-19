import asyncpg
import bcrypt
from typing import List
from src.models.user import UserCreate, User
from src.models.db.database import database
from datetime import datetime

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
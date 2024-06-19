import asyncpg # type: ignore
from typing import List
from src.api.models.user import User
from src.api.utils.database import database

async def get_users() -> List[User]:
    query = "SELECT name, email, phone, password, user_type, address, created_at, updated_at from users"
    rows = await database.connection.fetch(query)
    return [User(**dict(row)) for row in rows]
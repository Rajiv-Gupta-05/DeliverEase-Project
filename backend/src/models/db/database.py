import asyncpg # type: ignore
from .config import settings

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection = None

    async def connect(self):
        self.connection = await asyncpg.connect(self.dsn)
        print("Connected to database")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            print("Disconnected from database")

# Create a global database instance
database = Database(settings.database_url)

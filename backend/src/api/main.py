import asyncio
import asyncpg  # type: ignore
from fastapi import FastAPI
from src.api.config import settings

app = FastAPI()

class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None

    async def connect(self):
        self.connection = await asyncpg.connect(self.dsn)
        print("Connected to database")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            print("Disconnected from database")

# Database instance with the DSN from settings
database = Database(settings.database_url)

@app.on_event("startup")
async def on_startup():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Run the application with: uvicorn api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)

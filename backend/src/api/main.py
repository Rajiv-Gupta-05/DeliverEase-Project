from fastapi import FastAPI
from src.models.db.database import database # type: ignore
from src.api.routes import user, deliverer

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

app.include_router(user.router, prefix="/api")
app.include_router(deliverer.router, prefix="/api")

# Run the application with: uvicorn src.api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)

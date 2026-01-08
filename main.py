from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db import init_db
from src.moderation import load_model
from src import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    init_db()
    load_model()
    yield
    print("Shutting down...")

app = FastAPI(
    title="SafeSocial - ALBERT Moderated Chat",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "SafeSocial API running with clean architecture!"}
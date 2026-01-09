from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db import init_db
from src.moderation import load_model
from src import router

origins = ["*"]

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow these origins
    allow_credentials=True,
    allow_methods=["*"],        # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],        # allow headers like Authorization
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "SafeSocial API running with clean architecture!"}
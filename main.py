from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.api import auth, designs  # --- ADDED 'designs' ---
from app.models import user, design

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This ensures 'users' and 'designs' tables exist in garment_db
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Garment Platform Backend",
    description="Backend for the Design-to-Production Workflow",
    version="1.0.0",
    lifespan=lifespan
)

# Authentication Router
app.include_router(auth.router)

# --- ADD THIS LINE ---
# This makes POST /designs/ visible in Swagger
app.include_router(designs.router)

@app.get("/")
def health_check():
    return {
        "status": "Online",
        "environment": "Stable (Python 3.12)",
        "target_launch": "Q3 2026"
    }
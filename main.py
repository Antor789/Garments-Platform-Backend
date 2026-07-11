from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.api import auth, designs 
from app.models import user, design
from app.api import auth, designs, dashboard # <-- Include new dashboard module

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


# Setting allow_origins to ["*"] opens the API to the entire internet
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # ALLOW ALL: Any domain can fetch from this API
    allow_credentials=True,          # Note: Browsers ignore this if origins is "*"
    allow_methods=["*"],             # ALLOW ALL: POST, GET, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],             # ALLOW ALL: Content-Type, Authorization, etc.
)
# ---------------------------------------------------------------

# Authentication Router
app.include_router(auth.router)

# Designs Router (Visible in Swagger UI)
app.include_router(designs.router)

# Dashboard Router
app.include_router(dashboard.router)

@app.get("/")
def health_check():
    return {
        "status": "Online",
        "environment": "Stable (Python 3.12)",
        "target_launch": "Q3 2026"
    }
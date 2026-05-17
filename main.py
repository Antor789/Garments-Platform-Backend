from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORTED CORS MIDDLEWARE
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.api import auth, designs 
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

# ----------------- CORS CONFIGURATION -----------------
# Define the origins (frontends) that are allowed to access this API
origins = [
    "http://localhost:3000",  # Your local Next.js frontend running on your Dell laptop
    # Once you deploy your frontend, add its production URL here, e.g.:
    # "https://your-garments-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Grants access to listed domains
    allow_credentials=True,           # Allows passing cookies/credentials if needed
    allow_methods=["*"],              # Allows all standard HTTP methods: POST, GET, OPTIONS, etc.
    allow_headers=["*"],              # Allows all custom/standard headers
)
# ------------------------------------------------------

# Authentication Router
app.include_router(auth.router)

# Designs Router (Visible in Swagger UI)
app.include_router(designs.router)

@app.get("/")
def health_check():
    return {
        "status": "Online",
        "environment": "Stable (Python 3.12)",
        "target_launch": "Q3 2026"
    }
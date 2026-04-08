import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch the string you added to Vercel Settings
raw_url = os.environ.get("DATABASE_URL")

if raw_url:
    # Essential Fix: Force the '+psycopg' driver for Neon Cloud compatibility
    if raw_url.startswith("postgres://"):
        DATABASE_URL = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgresql://"):
        DATABASE_URL = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        DATABASE_URL = raw_url
else:
    # 2. Local fallback for your Dell Laptop (Offline mode)
    DATABASE_URL = "postgresql+psycopg://postgres:Antor789@localhost:5432/garment_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
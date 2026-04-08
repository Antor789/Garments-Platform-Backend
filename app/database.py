import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch the exact Value from Vercel
raw_url = os.environ.get("DATABASE_URL")

if raw_url:
    # Fix: Ensure the string starts with 'postgresql+psycopg://'
    # Neon and Vercel often provide 'postgres://' or 'postgresql://'
    # We must explicitly add the '+psycopg' driver for your setup.
    if raw_url.startswith("postgres://"):
        DATABASE_URL = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgresql://"):
        DATABASE_URL = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        DATABASE_URL = raw_url
else:
    # 2. Dell Laptop Fallback
    DATABASE_URL = "postgresql+psycopg://postgres:Antor789@localhost:5432/garment_db"

# Create engine with the corrected cloud URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
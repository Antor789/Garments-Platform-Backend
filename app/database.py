import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Explicitly look for the Vercel Environment Variable
# Use os.getenv to safely check if the cloud URL exists
raw_url = os.getenv("DATABASE_URL")

if raw_url and "127.0.0.1" not in raw_url:
    # Essential Fix: Neon and Vercel often provide 'postgres://' 
    # but SQLAlchemy 2.0+ requires 'postgresql+psycopg://'
    if raw_url.startswith("postgres://"):
        DATABASE_URL = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgresql://"):
        DATABASE_URL = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        DATABASE_URL = raw_url
else:
    # 2. Local fallback for your Dell Laptop (Offline development)
    # This ONLY runs if DATABASE_URL is missing or contains '127.0.0.1'
    DATABASE_URL = "postgresql+psycopg://postgres:Antor789@localhost:5432/garment_db"

# engine_kwargs can be used to handle pooled connections if needed later
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
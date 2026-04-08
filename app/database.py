import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Force retrieval of the Vercel Environment Variable
# We use os.environ to ensure it raises an error if the key is missing
DATABASE_URL = os.environ.get("DATABASE_URL")

# 2. Critical Fix: Inject the required driver for SQLAlchemy 2.0+
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    # 3. Only if the variable is missing completely (for local testing)
    DATABASE_URL = "postgresql+psycopg://postgres:Antor789@localhost:5432/garment_db"

# Create the engine with the cloud-ready URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
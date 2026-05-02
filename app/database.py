import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Load local .env (Vercel automatically ignores this)
load_dotenv()

# 2. Get the Cloud URL from Vercel Settings
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Fix: Ensure the string uses the correct driver for SQLAlchemy 2.0+
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    
    # Cloud Engine: pool_pre_ping prevents crashes during serverless cold starts
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    # 3. Local fallback using your separate .env keys
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD", "Antor789")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "garment_db")
    
    LOCAL_URL = f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(LOCAL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
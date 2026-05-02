import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Initialize environment variables
load_dotenv()

# 2. Logic to determine environment
# We check for 'DATABASE_URL' first. 
# On Vercel, this is your Neon Cloud string.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Essential Fix: SQLAlchemy 2.0.30+ requires 'postgresql+psycopg://'
    # Neon strings often come as 'postgres://' or 'postgresql://'
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    
    # PRODUCTION ENGINE:
    # 'pool_pre_ping' checks if the connection is still alive before using it.
    # This prevents the 'FUNCTION_INVOCATION_FAILED' crash during cold starts.
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    # 3. LOCAL FALLBACK:
    # Uses your separate confidential keys from the .env file.
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
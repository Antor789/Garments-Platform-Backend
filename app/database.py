from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Updated with your specific password and the psycopg3 driver
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:Antor789@localhost:5432/garment_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
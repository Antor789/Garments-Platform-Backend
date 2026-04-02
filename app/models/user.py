from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # "buyer" or "factory"
    
    # --- NEW PROFESSIONAL FIELDS ---
    full_name = Column(String, nullable=True) 
    phone_number = Column(String, unique=True, index=True, nullable=True)
    
    # Progress Trackers (For the "75% Complete" UI)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # --- RELATIONSHIP TO DESIGNS ---
    # This fixes the "Mapper[User(users)] has no property 'designs'" error.
    designs = relationship("Design", back_populates="creator", cascade="all, delete-orphan")
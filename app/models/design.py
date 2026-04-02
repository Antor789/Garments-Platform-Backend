from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

# Ensure this class name is exactly 'Design'
class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String)
    specifications = Column(JSON)
    creator_id = Column(Integer, ForeignKey("users.id"))

    # Establishes the link back to the User model
    creator = relationship("User", back_populates="designs")
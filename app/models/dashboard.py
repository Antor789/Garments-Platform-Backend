from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Factory(Base):
    __tablename__ = "factories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)  # e.g., "Vietnam • Tier 1 Partner"
    phase = Column(String)     # e.g., "Sampling Phase"

class ProductionOrder(Base):
    __tablename__ = "production_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False) # e.g., "#SC-88921"
    item_name = Column(String, nullable=False)                 # e.g., "Premium Heavyweight Tee"
    color_variant = Column(String)                             # e.g., "Bone White"
    total_value = Column(Float, nullable=False)                # $18,400.00
    escrow_secured = Column(Integer, default=1)                 # 1 = True, 0 = False
    current_stage = Column(String, default="FABRIC SOURCING")  # CUTTING & SEWING, etc.
    progress_percentage = Column(Integer, default=0)           # 65%
    est_delivery = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    factory_id = Column(Integer, ForeignKey("factories.id"))

    factory = relationship("Factory")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)        # "shipping", "escrow", "message"
    title = Column(String)       # "Shipping notification"
    description = Column(String) # "Order #SC-88710 has been dispatched..."
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
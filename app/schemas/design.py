from pydantic import BaseModel
from typing import Optional, Dict, Any

# Base fields shared by all Design schemas
class DesignBase(BaseModel):
    title: str # e.g., "Men's V-Neck T-Shirt"
    category: str # e.g., "Knitwear"
    specifications: Dict[str, Any] # Flexible JSON for measurements/fabric

# Schema for creating a new design
class DesignCreate(DesignBase):
    pass

# Schema for sending design data back to the frontend
class DesignResponse(DesignBase):
    id: int
    creator_id: int

    class Config:
        from_attributes = True
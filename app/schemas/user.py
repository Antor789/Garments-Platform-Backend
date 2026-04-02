from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "buyer" or "factory"
    
    # --- ADD THESE TO MATCH YOUR NEW DB COLUMNS ---
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    full_name: Optional[str]
    phone_number: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for the Bearer Token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for the data stored inside the JWT (usually the email)"""
    email: Optional[str] = None
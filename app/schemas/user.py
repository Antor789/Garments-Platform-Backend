from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr  # Enforces valid formatting (e.g., must contain '@' and a domain suffix)
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    role: str = "buyer"
    full_name: str = Field(..., min_length=1, description="Full name field cannot be blank")
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    full_name: str
    phone_number: Optional[str] = None
    is_email_verified: bool = False
    is_phone_verified: bool = False

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
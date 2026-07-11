from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User
from app.services.auth_service import AuthService
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# Corrected custom form wrapper
class OAuth2EmailRequestForm:
    def __init__(
        self,
        username: EmailStr = Form(),  # Use Form() instead of Depends() here
        password: str = Form(),
        grant_type: str = Form(default=None),
        scope: str = Form(default=""),
        client_id: str = Form(default=None),
        client_secret: str = Form(default=None),
    ):
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # 2. Check if phone number already exists
    if user_in.phone_number:
        phone_exists = db.query(User).filter(User.phone_number == user_in.phone_number).first()
        if phone_exists:
            raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # 3. Create new user with professional fields
    new_user = User(
        email=user_in.email,
        hashed_password=AuthService.hash_password(user_in.password),
        role=user_in.role,
        full_name=user_in.full_name,
        phone_number=user_in.phone_number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2EmailRequestForm = Depends(), db: Session = Depends(get_db)):
    # Resolves mapping mismatch by matching the text parameter to your PostgreSQL User.email table column
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not AuthService.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/onboarding-progress")
def get_onboarding_progress(current_user: User = Depends(get_current_user)):
    """
    Returns the percentage for the '75% Complete' bar in the Smart Garments UI.
    """
    steps = [
        {"name": "Verify Email", "completed": getattr(current_user, "is_email_verified", False)},
        {"name": "Complete Profile", "completed": bool(current_user.full_name)},
        {"name": "Verify Phone", "completed": getattr(current_user, "is_phone_verified", False)},
        {"name": "Set Up Payment", "completed": False} 
    ]
    
    completed_count = sum(1 for step in steps if step["completed"])
    percentage = int((completed_count / len(steps)) * 100)
    
    return {
        "progress_percentage": percentage,
        "checklist": steps
    }
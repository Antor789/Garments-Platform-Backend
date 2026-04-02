from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

# Configuration - Professional Note: Move these to a .env file later
SECRET_KEY = "garment-platform-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# The tokenUrl MUST match your router prefix + route path (e.g., /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    # Attributes for easy access in deps.py
    oauth2_scheme = oauth2_scheme
    SECRET_KEY = SECRET_KEY
    ALGORITHM = ALGORITHM

    @staticmethod
    def hash_password(password: str) -> str:
        """Secures passwords before they hit PostgreSQL"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """The critical check for the 'Authorize' button"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict):
        """Generates the identity token for the Smart Garments UI"""
        to_encode = data.copy()
        # Use timezone-aware UTC for modern Python 3.12 standards
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
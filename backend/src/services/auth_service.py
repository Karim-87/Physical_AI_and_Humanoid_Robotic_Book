from datetime import datetime, timedelta
from typing import Optional
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from ..config.settings import settings
from ..models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import or_


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = db.query(User).filter(
            or_(User.username == username, User.email == username)
        ).first()

        if not user or not self.verify_password(password, user.password_hash):
            return None

        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token."""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def get_current_user(self, db: Session, token: str) -> Optional[User]:
        """Get the current user from the token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None

        user = db.query(User).filter(User.username == username).first()
        return user

    def create_user(self, db: Session, username: str, email: str, password: str) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        # Hash the password
        hashed_password = self.get_password_hash(password)

        # Create the user
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
"""Handles business logic for user authentication"""

import hashlib
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.settings import JWTConfig
from src.database.models import User

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def create_token(email: str):
        payload = {
            "sub": email,
            "exp": datetime.utcnow() + timedelta(seconds=JWTConfig.EXPIRATION_SECONDS)
        }
        return jwt.encode(payload, JWTConfig.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, JWTConfig.SECRET_KEY, algorithms=["HS256"])
            return payload["sub"]
        except Exception as e:
            return None

    def authenticate_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user and user.hashed_password == self.hash_password(password):
            return user
        return None

    def register_user(self, first_name, last_name, email, password):
        if self.db.query(User).filter(User.email == email).first():
            return None
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=self.hash_password(password)
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
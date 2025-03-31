# app/models.py
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.databases import Base

# ---------------------------------
# ✅ SQLAlchemy Models (DB Tables)
# ---------------------------------

# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ---------------------------------
# ✅ Pydantic Models (Validation)
# ---------------------------------

# Base model for User
class UserBase(BaseModel):
    username: str
    email: EmailStr


# Model for user registration
class UserCreate(UserBase):
    password: str


# Model for API response
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ Pydantic v2 compatibility


# Model for authentication token
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data model
class TokenData(BaseModel):
    username: Optional[str] = None

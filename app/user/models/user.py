from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel

from app.db.base import BaseTable


class UserBase(SQLModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    is_verified: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class User(BaseTable, UserBase, table=True):
    hashed_password : str

from typing import Optional
from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: Optional[int] = None
    groups: Optional[list] = None
    permissions: Optional[list] = None


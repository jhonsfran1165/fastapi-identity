from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime


class BaseTable(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    )

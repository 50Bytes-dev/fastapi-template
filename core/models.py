import re
from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlalchemy import text
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class BaseTableName(SQLModel):
    @classmethod
    @property
    def __tablename__(cls):
        class_name = cls.__name__
        words = re.findall("[A-Z][^A-Z]*", class_name)
        return "_".join([word.lower() for word in words])


class BaseTable(BaseTableName):
    id: int = Field(
        default=None,
        primary_key=True,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )

    @field_validator("updated_at")
    def validate_updated_at(cls, v):
        if v is None:
            return v
        return v.replace(tzinfo=None)

    async def save(self, db_session: AsyncSession):
        db_session.add(self)
        await db_session.commit()
        await db_session.refresh(self)
        return self

    async def delete(self, db_session: AsyncSession):
        await db_session.delete(self)
        await db_session.commit()
        return True

    async def update(self, db_session: AsyncSession, commit: bool = False, **kwargs):
        self.model_update(**kwargs)
        db_session.add(self)
        await db_session.commit()
        await db_session.refresh(self)
        return self

    def model_update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

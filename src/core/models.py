from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.now},
    )


class ResponseCode(str, Enum):
    success = "SUCCESS"
    data_not_found = "DATA_NOT_FOUND"
    bad_request = "BAD_REQUEST"
    already_exists = "ALREADY_EXIST"
    unauthorized = "UNAUTHORIZED"


class Response(SQLModel):
    success: bool = True
    response_code: ResponseCode
    message: str = ""
    data: dict | list[dict] = {}

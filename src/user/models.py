from enum import Enum

from src.core.models import BaseModel
from sqlmodel import Field, SQLModel


class UserType(str, Enum):
    employer = "EMPLOYER"
    job_seeker = "JOB_SEEKER"
    admin = "ADMIN"


class UserSource(str, Enum):
    self = "SELF"
    google = "GOOGLE"
    linkedin = "LINKEDIN"


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, index=True)
    first_name: str = Field(nullable=False)
    last_name: str
    password: str | None = Field(default=None)
    role: UserType
    is_verified: bool = False
    is_active: bool = True
    source: str = Field(nullable=True, default=UserSource.self)


class User(BaseModel, UserBase):
    pass


class VerifyUser(SQLModel):
    access_token: str


class VerifyTokenResponse(SQLModel):
    success: bool = True
    message: str = "success"
    user_id: str | None = None

# Define relationship types
from datetime import date, datetime
import enum
from typing import List, Optional
from datetime import timezone
from uuid import UUID
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from src.core.models import BaseSQLModel


class RelationType(str, enum.Enum):
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    GRANDPARENT = "grandparent"
    GRANDCHILD = "grandchild"
    UNCLE_AUNT = "uncle_aunt"
    NIECE_NEPHEW = "niece_nephew"
    COUSIN = "cousin"
    OTHER = "other"


# Models
class FamilyRelationshipBase(SQLModel):
    relation_type: RelationType = Field(...)


class FamilyRelationship(BaseSQLModel, FamilyRelationshipBase, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    relative_id: UUID = Field(foreign_key="user.id")


class UserBase(SQLModel):
    first_name: str
    last_name: str
    dob: str = Field(...)
    mobile: str = Field(regex="^[0-9]{10}$", unique=True)
    is_parent: bool = Field(default=False)

    @field_validator("dob")
    def validate_dob_format(cls, value):
        try:
            # Check if the date is in the format YYYY-MM-DD
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date of birth must be in the format YYYY-MM-DD")
        return value


class User(BaseSQLModel, UserBase, table=True):
    # Relationships
    # relationships: List["FamilyRelationship"] = Relationship(
    #     back_populates="user",
    # )

    def age(self) -> int:
        today = date.today()
        parsed_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (
            today.year
            - parsed_date.year
            - ((today.month, today.day) < (parsed_date.month, parsed_date.day))
        )


# Request/Response Models
class UserCreate(UserBase):
    pass


class FamilyMemberCreate(UserBase):
    relation_type: RelationType


class OTPBase(SQLModel):
    mobile: str = Field(regex="^[0-9]{10}$")
    otp_code: str
    is_verified: bool = Field(default=False)


class OTP(BaseSQLModel, OTPBase, table=True):
    expires_at: datetime


class OTPRequest(SQLModel):
    mobile: str = Field(regex="^[0-9]{10}$")


class OTPVerify(OTPRequest):
    otp: str = Field(regex="^[0-9]{6}$")

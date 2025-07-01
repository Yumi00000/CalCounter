from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, SecretStr
from typing import Optional, Any
from datetime import datetime
from pyobjectID import PyObjectId

from backend.app.databade.database import db

collection = db["users"]


class UserCreate(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    age: int

    @field_validator("age")
    def validate_age(cls, v):
        if v < 18:
            raise ValueError("You must be at least 18 years old")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v) or \
                not any(c.islower() for c in v) or \
                not any(c.isdigit() for c in v) or \
                len(v) < 8:
            raise ValueError("Password validation error")
        return v


class UserInDB(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    age: int
    weight: Optional[float] = None
    height: Optional[int] = None
    sex: Optional[str] = None
    active: bool
    user_goal_id: Optional[PyObjectId] = None
    created: datetime

    @model_validator(mode="before")
    def check_non_negative(cls, values: dict[str, Any]) -> dict[str, Any]:
        for field_name in ["height", "weight", "age"]:
            value = values.get(field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} must be non-negative")
        return values

    @field_validator("sex")
    def sex_must_be_valid(cls, v):
        valid_sex = ["M", "F", "Other"]
        if v not in valid_sex:
            raise ValueError(f"Sex must be one of {valid_sex}")
        return v


class UserPublic(BaseModel):
    username: str
    weight: float
    height: int
    sex: str
    user_goal_id: PyObjectId
    created: datetime


collection.create_index("email", unique=True)

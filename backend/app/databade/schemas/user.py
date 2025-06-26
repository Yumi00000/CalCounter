from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, Any
from datetime import datetime

from pyobjectID import PyObjectId

from backend.app.databade.database import db

collection = db["users"]


class UserCreate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    age: int
    weight: float
    height: int
    sex: str
    user_goal_id: PyObjectId

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


class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    active: bool
    full_name: Optional[str]
    age: int
    weight: float
    height: int
    sex: str
    user_goal_id: PyObjectId
    created: datetime


collection.create_index("email", unique=True)

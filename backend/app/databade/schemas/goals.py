from typing import Any

from pydantic import BaseModel, Field, model_validator

from pyobjectID import PyObjectId

from backend.app.databade.database import db

collection = db["user_goals"]


class UserGoalCreate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    weight: float
    calories: int
    daily_achieve_ids: list[PyObjectId] = []

    @model_validator(mode="before")
    def check_non_negative(cls, values: dict[str, Any]) -> dict[str, Any]:
        for field_name in ["calories", "weight"]:
            value = values.get(field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} must be non-negative")
        return values


collection.create_index("user_goal_id")

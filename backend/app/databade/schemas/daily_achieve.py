from typing import Any

from pydantic import BaseModel, Field, model_validator
from pyobjectID import PyObjectId

from backend.app.databade.database import db

collection = db["user_daily_achieve"]


class UserGoalsDailyCreate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    calories: int
    carbs: float
    fats: float
    protein: float
    fiber: float
    saturated_fat: float
    sugar: float
    meals_id: list[PyObjectId] = []

    @model_validator(mode="before")
    def check_non_negative(cls, values: dict[str, Any]) -> dict[str, Any]:
        for field_name in ["calories", "carbs", "fats", "protein", "fiber", "saturated_fat", "sugar"]:
            value = values.get(field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} must be non-negative")
        return values


class UserGoalsDailyOut(BaseModel):
    id: str = Field(..., alias="_id")
    remaining_cal: int
    burned_ca: int
    consumed_cal: int
    remaining_carbs: float
    remaining_fats: float
    remaining_protein: float
    remaining_fiber: float
    remaining_saturated_fat: float
    remaining_sugar: float

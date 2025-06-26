from datetime import datetime
from typing import Any

from pyobjectID import PyObjectId
from pydantic import BaseModel, Field, model_validator

from backend.app.databade.database import db

collection = db["daily_meals"]


class DailyMealsCreate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    calories: int
    carbs: float
    fats: float
    protein: float
    fiber: float
    saturated_fat: float
    sugar: float

    @model_validator(mode="before")
    def check_non_negative(cls, values: dict[str, Any]) -> dict[str, Any]:
        for field_name in ["calories", "carbs", "fats", "protein", "fiber", "saturated_fat", "sugar"]:
            value = values.get(field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} must be non-negative")
        return values


class DailyMealsOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    calories: int
    carbs: float
    fats: float
    protein: float
    source: str
    ate_at: datetime

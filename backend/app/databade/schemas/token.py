from typing import Optional

from pydantic import BaseModel

from backend.app.databade.database import db

collection = db["jwt_token"]

class Token(BaseModel):
    user_identifier: Optional[str] = None
    access_token: str
    token_type: str




class TokenData(BaseModel):
    identifier: Optional[str] = None

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserRatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int = Field(ge=0, le=10, description="Rating from 0.0 to 10")
    comment: Optional[str] = None

class UserRatingUpdate(BaseModel):
    rating: int = Field(ge=0, le=10, description="Rating from 0.0 to 10")

class UserRatingOut(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
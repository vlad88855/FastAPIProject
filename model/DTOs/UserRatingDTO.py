from pydantic import BaseModel, Field, ConfigDict

class UserRatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int = Field(ge=0, le=10, description="Rating from 0.0 to 10")

class UserRatingUpdate(BaseModel):
    rating: int = Field(ge=0, le=10, description="Rating from 0.0 to 10")

class UserRatingOut(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int

    model_config = ConfigDict(from_attributes=True)
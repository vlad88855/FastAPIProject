from pydantic import BaseModel

class UserRating(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating: float
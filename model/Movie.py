from typing import List
from pydantic import BaseModel
from model import UserRating

class Movie(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    view_count: int = 0


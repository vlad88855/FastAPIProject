from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

import enum

class MovieGenre(str, enum.Enum):
    FANTASTIC = "fantastic"
    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"
    HORROR = "horror"
    SCI_FI = "sci-fi"
    THRILLER = "thriller"

class MovieCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255, description="Movie title")
    year: int = Field(ge=1900, le=datetime.now().year, description="Movie year")
    genre: MovieGenre = Field(description="Movie genre")

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    genre: Optional[MovieGenre] = None
    view_count: Optional[int] = None

class MovieOut(BaseModel):
    id: int
    title: str
    year: int
    genre: MovieGenre
    view_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)
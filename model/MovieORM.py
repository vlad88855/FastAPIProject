# model/MovieORM.py
from sqlalchemy import Column, Integer, String, UniqueConstraint, Enum, Float, Text
from db import Base
from model.DTOs.MovieDTO import MovieGenre


class MovieORM(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(Enum(MovieGenre), nullable=False)
    average_rating = Column(Float, nullable=False, default=0.0)
    view_count = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=True)
    director = Column(String(255), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    poster_url = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("title", name="uq_movies_title"),
    )
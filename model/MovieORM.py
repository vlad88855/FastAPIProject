# model/MovieORM.py
from sqlalchemy import Column, Integer, String, UniqueConstraint, Enum
from db import Base
from model.DTOs.MovieDTO import MovieGenre


class MovieORM(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(Enum(MovieGenre), nullable=False)
    view_count = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("title", name="uq_movies_title"),
    )
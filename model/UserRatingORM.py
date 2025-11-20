# model/UserRatingORM.py
from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from db import Base


class UserRatingORM(Base):
    __tablename__ = "user_ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_user_movie_rating"),
    )
from abc import ABC, abstractmethod
from typing import Dict, Type
from sqlalchemy.orm import Session
from sqlalchemy import func
from model.UserRatingORM import UserRatingORM
from model.MovieORM import MovieORM

class BaseAchievementHandler(ABC):
    @abstractmethod
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        pass

class ReviewCountHandler(BaseAchievementHandler):
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        threshold = params.get("threshold", 0)
        count = db.query(func.count(UserRatingORM.id)).filter(UserRatingORM.user_id == user_id).scalar()
        return count >= threshold

class GenreMasterHandler(BaseAchievementHandler):
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        genre = params.get("genre")
        threshold = params.get("threshold", 0)
        
        if not genre:
            return False

        count = (
            db.query(func.count(UserRatingORM.id))
            .join(MovieORM, UserRatingORM.movie_id == MovieORM.id)
            .filter(UserRatingORM.user_id == user_id, MovieORM.genre == genre)
            .scalar()
        )
        return count >= threshold
class CommentHandler(BaseAchievementHandler):
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        comment = params.get("comment")
        threshold = params.get("threshold", 0)
class CommentCountHandler(BaseAchievementHandler):
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        threshold = params.get("threshold", 0)
        count = db.query(func.count(UserRatingORM.id)).filter(
            UserRatingORM.user_id == user_id,
            UserRatingORM.comment.isnot(None)
        ).scalar()
        return count >= threshold

class DistinctGenreHandler(BaseAchievementHandler):
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        threshold = params.get("threshold", 0)
        count = db.query(func.count(func.distinct(MovieORM.genre))).join(
            UserRatingORM, UserRatingORM.movie_id == MovieORM.id
        ).filter(UserRatingORM.user_id == user_id).scalar()
        return count >= threshold

class ContrarianHandler(BaseAchievementHandler):
    def check(self, user_id: int, params: dict, db: Session) -> bool:
        min_user_rating = params.get("min_user_rating", 10)
        max_movie_avg = params.get("max_movie_avg", 5.0)
        threshold = params.get("threshold", 1)
        
        count = db.query(func.count(UserRatingORM.id)).join(
            MovieORM, UserRatingORM.movie_id == MovieORM.id
        ).filter(
            UserRatingORM.user_id == user_id,
            UserRatingORM.rating >= min_user_rating,
            MovieORM.average_rating < max_movie_avg
        ).scalar()
        
        return count >= threshold

class HandlerRegistry:
    _handlers: Dict[str, BaseAchievementHandler] = {}

    @classmethod
    def register(cls, condition_type: str, handler: BaseAchievementHandler):
        cls._handlers[condition_type] = handler

    @classmethod
    def get_handler(cls, condition_type: str) -> BaseAchievementHandler:
        return cls._handlers.get(condition_type)

HandlerRegistry.register("COUNT_REVIEWS", ReviewCountHandler())
HandlerRegistry.register("GENRE_MASTER", GenreMasterHandler())
HandlerRegistry.register("COMMENT_COUNT", CommentCountHandler())
HandlerRegistry.register("DISTINCT_GENRE", DistinctGenreHandler())
HandlerRegistry.register("CONTRARIAN", ContrarianHandler())

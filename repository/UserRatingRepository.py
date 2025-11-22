import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


from model.UserRatingORM import UserRatingORM
from model.DTOs.UserRatingDTO import UserRatingCreate, UserRatingUpdate
from repository.exceptions import UserRatingNotFoundException, UserRatingExistsException


class UserRatingRepository():

    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)


    def create_rating(self, dto: UserRatingCreate) -> UserRatingORM:
        try:
            rating = UserRatingORM(
                user_id=dto.user_id,
                movie_id=dto.movie_id,
                rating=dto.rating
            )
            self.db.add(rating)
            self.db.commit()
            self.db.refresh(rating)
            self.logger.info(f"Created rating for user {dto.user_id} on movie {dto.movie_id}")
            return rating
        except IntegrityError as e:
            self.logger.error(f"Error creating rating: {e}")
            self.db.rollback()
            if "uq_user_movie_rating" in str(e.orig).lower():
                raise UserRatingExistsException(
                    f"User {dto.user_id} rating for movie {dto.movie_id} already exists"
                )
            raise e

    def delete_rating(self, id: int) -> None:
        rating = self.get_rating(id)
        self.db.delete(rating)
        self.db.commit()
        self.logger.info(f"Deleted rating with ID: {id}")

    def delete_all_ratings(self) -> None:
        self.db.query(UserRatingORM).delete()
        self.db.commit()
        self.logger.info("Deleted all ratings.")

    def get_rating(self, id: int) -> UserRatingORM:
        rating = self.db.get(UserRatingORM, id)
        if not rating:
            raise UserRatingNotFoundException(f"UserRating {id} not found")
        return rating

    def find_rating_by_user_movie(self, user_id: int, movie_id: int) -> UserRatingORM | None:
        return self.db.query(UserRatingORM).filter_by(
            user_id=user_id,
            movie_id=movie_id
        ).first()

    def get_all_ratings(self) -> list[UserRatingORM]:
        return self.db.query(UserRatingORM).all()

    def update_rating(self, id: int, dto: UserRatingUpdate) -> UserRatingORM:
        rating = self.get_rating(id)
        rating.rating = dto.rating

        self.db.commit()
        self.db.refresh(rating)
        self.logger.info(f"Updated rating with ID: {id}")
        return rating

    def get_average_rating(self, movie_id: int) -> float:
        avg_rating = self.db.query(func.avg(UserRatingORM.rating)).filter(UserRatingORM.movie_id == movie_id).scalar()
        return float(avg_rating) if avg_rating is not None else 0.0
import logging
from typing import Optional, List
from model.DTOs.UserRatingDTO import UserRatingOut, UserRatingUpdate, UserRatingCreate
from repository.MovieRepository import MovieRepository
from repository.UserRatingRepository import UserRatingRepository
from repository.UserRepository import UserRepository
from repository.exceptions import UserRatingExistsException
from service.AchievementService import AchievementService


class UserRatingService:

    def __init__(self, rating_repo: UserRatingRepository, user_repo: UserRepository, movie_repo: MovieRepository, achievement_service: AchievementService):
        self.rating_repo = rating_repo
        self.user_repo = user_repo
        self.movie_repo = movie_repo
        self.achievement_service = achievement_service
        self.logger = logging.getLogger(__name__)

    def create_rating(self, dto: UserRatingCreate) -> UserRatingOut:
        self.user_repo.get_user(dto.user_id)
        self.movie_repo.get_movie(dto.movie_id)

        existing_rating = self.rating_repo.find_rating_by_user_movie(dto.user_id, dto.movie_id)
        if existing_rating:
            self.logger.warning(f"Rating creation failed: User {dto.user_id} already rated movie {dto.movie_id}")
            raise UserRatingExistsException(
                f"User {dto.user_id} rating for movie {dto.movie_id} already exists"
            )

        rating_obj = self.rating_repo.create_rating(dto)
        
        self.achievement_service.check_new_achievements(dto.user_id)
        
        return UserRatingOut.model_validate(rating_obj)

    def delete_rating(self, id: int) -> None:
        self.rating_repo.delete_rating(id)

    def get_rating(self, id: int) -> UserRatingOut:
        rating_obj = self.rating_repo.get_rating(id)
        return UserRatingOut.model_validate(rating_obj)

    def get_all_ratings(self) -> List[UserRatingOut]:
        ratings = self.rating_repo.get_all_ratings()
        return [UserRatingOut.model_validate(r) for r in ratings]

    def update_rating(self, id: int, dto: UserRatingUpdate) -> UserRatingOut:
        rating_obj = self.rating_repo.update_rating(id, dto)
        return UserRatingOut.model_validate(rating_obj)

    def delete_all_ratings(self) -> None:
        self.rating_repo.delete_all_ratings()
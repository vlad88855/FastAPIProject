from repository.MovieRepository import MovieRepository
from repository.UserRatingRepository import UserRatingRepository
from model.UserRating import UserRating
from repository.UserRepository import UserRepository
from repository.exceptions import UserRatingExistsException


class UserRatingService():

    @classmethod
    def create_user_rating(cls, movie_id: int, user_id: int, rating: float) -> UserRating:
        UserRepository.get_user(user_id)
        MovieRepository.get_movie(movie_id)
        user_rating = UserRatingRepository.find_user_rating_by_sec_key(user_id, movie_id)
        if user_rating:
            raise UserRatingExistsException()
        return UserRatingRepository.create_user_rating(movie_id, user_id, rating)


    @classmethod
    def delete_user_rating(cls, id: int):
        return UserRatingRepository.delete_user_rating(id)

    @classmethod
    def get_user_rating(cls, id: int) -> UserRating | None:
        return UserRatingRepository.get_user_rating(id)

    @classmethod
    def get_all_user_ratings(cls) -> dict:
        return UserRatingRepository.get_all_user_ratings()

    @classmethod
    def update_user_rating(cls, id: int, rating: float) -> UserRating | None:
        return UserRatingRepository.update_user_rating(id, rating)

    @classmethod
    def delete_all_user_ratings(cls):
        UserRatingRepository.delete_all_user_ratings()
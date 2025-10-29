from model.UserRating import UserRating
from repository.exceptions import UserRatingNotFoundException


class UserRatingRepository():
    user_rating_id_counter: int = 0
    user_ratings = {}

    @classmethod
    def create_user_rating(cls, movie_id: int, user_id: int, rating: float) -> UserRating:
        cls.user_rating_id_counter += 1
        user_rating = UserRating(id=cls.user_rating_id_counter, movie_id=movie_id, user_id=user_id, rating=rating)
        cls.user_ratings[cls.user_rating_id_counter] = user_rating
        return user_rating

    @classmethod
    def delete_user_rating(cls, id:int) -> None:
        user_rating = cls.get_user_rating(id)
        cls.user_ratings.pop(user_rating.id)

    @classmethod
    def delete_all_user_ratings(cls):
        cls.user_ratings.clear()

    @classmethod
    def get_user_rating(cls, id:int) -> UserRating:
        user_rating = cls.user_ratings.get(id)
        if not user_rating:
            raise UserRatingNotFoundException(f"UserRating {id} not found")
        return user_rating

    @classmethod
    def find_user_rating_by_sec_key(cls, user_id: int, movie_id: int) -> UserRating | None:
        for user_rating in cls.user_ratings.values():
            if user_rating.user_id == user_id and user_rating.movie_id == movie_id:
                return user_rating
        return None

    @classmethod
    def get_all_user_ratings(cls) -> list[UserRating]:
        return list(cls.user_ratings.values())

    @classmethod
    def update_user_rating(cls, id: int, rating: float):
        user_rating = cls.get_user_rating(id)
        user_rating.rating = rating

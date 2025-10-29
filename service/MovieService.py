from model import Movie
from repository.MovieRepository import MovieRepository
from repository.UserRepository import UserRepository


class MovieService():

    @classmethod
    def create_movie(cls, title: str, year:int, genre: str, view_count: int | None = None) -> Movie:
        return MovieRepository.create_movie(title, year, genre, view_count)

    @classmethod
    def delete_movie(cls, id: int):
        MovieRepository.delete_movie(id)

    @classmethod
    def get_movie(cls, id: int) -> Movie:
        return MovieRepository.get_movie(id)

    @classmethod
    def get_all_movies(cls) -> dict:
        return MovieRepository.get_all_movies()

    @classmethod
    def update_movie(cls, id: int, title: str, year:int, genre: str, view_count: int | None = None) -> Movie:
        return MovieRepository.update_movie(id, title, year, genre, view_count)
    @classmethod
    def delete_all_movies(cls):
        MovieRepository.delete_all_movies()
    @classmethod
    def watch_movie(cls, movie_id: int, user_id: int) -> Movie:
        # Необхідна перевірка на унікальність користувача
        UserRepository.get_user(user_id)
        MovieRepository.increment_view_count(movie_id)

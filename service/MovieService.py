from model import MovieORM
from model.DTOs.MovieDTO import MovieCreate, MovieUpdate, MovieOut
from repository.MovieRepository import MovieRepository
from repository.UserRepository import UserRepository


class MovieService():

    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def create_movie(self, dto: MovieCreate) -> MovieOut:
        movie = self.repository.create_movie(dto)
        return MovieOut.model_validate(movie)

    def get_movie(self, id: int) -> MovieOut:
        movie = self.repository.get_movie(id)
        return MovieOut.model_validate(movie)

    def get_all_movies(self) -> list[MovieOut]:
        movies = self.repository.get_all_movies()
        return [MovieOut.model_validate(movie) for movie in movies]

    def update_movie(self, id: int, dto: MovieUpdate) -> MovieOut:
        movie = self.repository.update_movie(id, dto)
        return MovieOut.model_validate(movie)

    def delete_movie(self, id: int) -> None:
        self.repository.delete_movie(id)

    def delete_all_movies(self) -> None:
        self.repository.delete_all_movies()
    # def watch_movie(self, movie_id: int, user_id: int) -> Movie:
    #     # Необхідна перевірка на унікальність користувача
    #     UserRepository.get_user(user_id)
    #     MovieRepository.increment_view_count(movie_id)

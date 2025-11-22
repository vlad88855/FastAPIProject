from typing import Optional
from model import MovieORM
from model.DTOs.MovieDTO import MovieCreate, MovieUpdate, MovieOut, MovieGenre
from repository.MovieRepository import MovieRepository
from repository.UserRepository import UserRepository
from repository.UserRatingRepository import UserRatingRepository
from service.CacheService import CacheService
from service.ConfigService import ConfigService


class MovieService():

    def __init__(self, repository: MovieRepository, rating_repository: UserRatingRepository, cache: CacheService, config: ConfigService):
        self.repository = repository
        self.rating_repository = rating_repository
        self.cache = cache
        self.config = config

    def create_movie(self, dto: MovieCreate) -> MovieOut:
        movie = self.repository.create_movie(dto)
        self.cache.clear_all_starting_with("movies_")
        return MovieOut.model_validate(movie)

    def get_movie(self, id: int) -> MovieOut:
        movie = self.repository.get_movie(id)
        return MovieOut.model_validate(movie)

    def get_all_movies(self, skip: int = 0, limit: Optional[int] = None, genre: Optional[MovieGenre] = None) -> list[MovieOut]:
        if limit is None:
            limit = self.config.get("default_page_size", 10)
            
        cache_key = f"movies_skip_{skip}_limit_{limit}_genre_{genre}"
        cached_data = self.cache.get(cache_key)
        if cached_data is not None:
            return cached_data
            
        if genre:
            movies = self.repository.get_by_genre(genre, skip, limit)
        else:
            movies = self.repository.get_paginated(skip, limit)
            
        result = [MovieOut.model_validate(movie) for movie in movies]
        
        self.cache.set(cache_key, result)
        return result

    def update_movie(self, id: int, dto: MovieUpdate) -> MovieOut:
        movie = self.repository.update_movie(id, dto)
        self.cache.clear_all_starting_with("movies_")
        return MovieOut.model_validate(movie)

    def delete_movie(self, id: int) -> None:
        self.repository.delete_movie(id)
        self.cache.clear_all_starting_with("movies_")

    def delete_all_movies(self) -> None:
        self.repository.delete_all_movies()
        self.cache.clear_all_starting_with("movies_")

    def get_movie_rating(self, movie_id: int) -> float:
        # Ensure movie exists
        self.repository.get_movie(movie_id)
        return self.rating_repository.get_average_rating(movie_id)
    # def watch_movie(self, movie_id: int, user_id: int) -> Movie:
    #     # Необхідна перевірка на унікальність користувача
    #     UserRepository.get_user(user_id)
    #     MovieRepository.increment_view_count(movie_id)

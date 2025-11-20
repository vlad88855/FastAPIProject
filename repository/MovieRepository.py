import logging
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.MovieORM import MovieORM
from model.DTOs.MovieDTO import MovieCreate, MovieUpdate, MovieGenre
from repository.exceptions import MovieNotFoundException, MovieTitleExistsException


class MovieRepository():
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def create_movie(self, dto: MovieCreate) -> MovieORM:
        try:
            movie = MovieORM(title=dto.title, year=dto.year, genre=dto.genre)
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            self.logger.info(f"Created movie: {movie.title}")
            return movie
        except IntegrityError as e:
            self.db.rollback()
            msg = str(e.orig).lower()
            if "uq_movies_title" in msg or "title" in msg:
                raise MovieTitleExistsException(f"Movie {dto.title} already exists")
            raise e

    def get_movie(self, id: int) -> MovieORM:
        movie = self.db.get(MovieORM, id)
        if not movie:
            raise MovieNotFoundException(f"Movie {id} not found")
        return movie
    
    def get_all(self) -> List[MovieORM]:
        self.logger.info("Fetching all movies")
        return self.db.query(MovieORM).all()

    def get_paginated(self, skip: int, limit: int) -> List[MovieORM]:
        self.logger.info(f"Fetching movies with skip={skip}, limit={limit}")
        return self.db.query(MovieORM).offset(skip).limit(limit).all()

    def get_by_genre(self, genre: MovieGenre, skip: int, limit: int) -> List[MovieORM]:
        self.logger.info(f"Fetching movies with genre={genre}, skip={skip}, limit={limit}")
        return self.db.query(MovieORM).filter(MovieORM.genre == genre).offset(skip).limit(limit).all()

    def update_movie(self, id: int, dto: MovieUpdate) -> MovieORM:
        try:
            movie = self.get_movie(id)
            if dto.title is not None:
                movie.title = dto.title
            if dto.year is not None:
                movie.year = dto.year
            if dto.genre is not None:
                movie.genre = dto.genre
            self.db.commit()
            self.db.refresh(movie)
        except IntegrityError as e:
            self.db.rollback()
            msg = str(e.orig).lower()
            if "uq_movies_title" in msg or "title" in msg:
                raise MovieTitleExistsException(f"Movie {dto.title} already exists")
            raise e
        return movie

    def delete_movie(self, id: int) -> None:
        movie = self.get_movie(id)
        self.db.delete(movie)
        self.db.commit()
            
    def delete_all_movies(self) -> None:
        self.db.query(MovieORM).delete()
        self.db.commit()
    
    def increment_view_count(self, id: int) -> MovieORM:
        movie = self.get_movie(id)
        movie.view_count += 1
        self.db.commit()
        self.db.refresh(movie)
        return movie
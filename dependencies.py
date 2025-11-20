from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db

from service.ConfigService import ConfigService
from service.CacheService import CacheService
from service.MovieService import MovieService
from service.UserService import UserService
from service.AchievementService import AchievementService
from service.UserRatingService import UserRatingService

from repository.MovieRepository import MovieRepository
from repository.UserRepository import UserRepository
from repository.UserRatingRepository import UserRatingRepository

# Config
def get_config_service() -> ConfigService:
    return ConfigService()

# Cache
def get_cache_service(config: ConfigService = Depends(get_config_service)) -> CacheService:
    return CacheService(config)

# Repositories
def get_movie_repo(db: Session = Depends(get_db)) -> MovieRepository:
    return MovieRepository(db)

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_rating_repo(db: Session = Depends(get_db)) -> UserRatingRepository:
    return UserRatingRepository(db)

# Services
def get_movie_service(
    repo: MovieRepository = Depends(get_movie_repo),
    cache: CacheService = Depends(get_cache_service),
    config: ConfigService = Depends(get_config_service)
) -> MovieService:
    return MovieService(repo, cache, config)

def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
    config: ConfigService = Depends(get_config_service)
) -> UserService:
    return UserService(repo, config)

def get_achievement_service(db: Session = Depends(get_db)) -> AchievementService:
    return AchievementService(db)

def get_user_rating_service(
    rating_repo: UserRatingRepository = Depends(get_rating_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    movie_repo: MovieRepository = Depends(get_movie_repo),
    achievement_service: AchievementService = Depends(get_achievement_service)
) -> UserRatingService:
    return UserRatingService(rating_repo, user_repo, movie_repo, achievement_service)

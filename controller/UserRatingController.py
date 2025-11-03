from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db

from service.UserRatingService import UserRatingService

router = APIRouter()

@router.get("/userRating/{id}")
async def get_userRating(id: int):
    return UserRatingService.get_user_rating(id)

@router.post("/userRating")
async def create_userRating(movie_id: int, user_id: int, rating: float):
    return UserRatingService.create_user_rating(movie_id, user_id, rating)

@router.put("/userRating/{id}")
async def update_userRating(id: int, rating: float):
    return UserRatingService.update_user_rating(id, rating)

@router.delete("/userRating/{id}")
async def delete_userRating(id: int):
    return UserRatingService.delete_user_rating(id)

@router.get("/userRating")
async def get_userRatings():
    return UserRatingService.get_all_user_ratings()
@router.delete("/userRating")
async def delete_all_user_ratings():
    return UserRatingService.delete_all_user_ratings()
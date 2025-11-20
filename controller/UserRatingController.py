from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

from model.DTOs.UserRatingDTO import UserRatingCreate, UserRatingOut, UserRatingUpdate
from dependencies import get_user_rating_service
from service.UserRatingService import UserRatingService
from service.AchievementService import AchievementService
from repository.UserRatingRepository import UserRatingRepository
from repository.UserRepository import UserRepository
from repository.MovieRepository import MovieRepository

router = APIRouter(tags=["User Ratings methods"])

@router.post("/userRating", response_model=UserRatingOut)
async def create_userRating(
    dto: UserRatingCreate,
    service: UserRatingService = Depends(get_user_rating_service)
):
    return service.create_rating(dto)

@router.get("/userRating/{id}", response_model=UserRatingOut)
async def get_userRating(
    id: int,
    service: UserRatingService = Depends(get_user_rating_service)
):
    return service.get_rating(id)

@router.put("/userRating/{id}", response_model=UserRatingOut)
async def update_userRating(
    id: int,
    dto: UserRatingUpdate,
    service: UserRatingService = Depends(get_user_rating_service)
):
    return service.update_rating(id, dto)

@router.delete("/userRating/{id}")
async def delete_userRating(
    id: int,
    service: UserRatingService = Depends(get_user_rating_service)
):
    service.delete_rating(id)

@router.get("/userRating", response_model=List[UserRatingOut])
async def get_userRatings(
    service: UserRatingService = Depends(get_user_rating_service)
):
    return service.get_all_ratings()

@router.delete("/userRating")
async def delete_all_user_ratings(
    service: UserRatingService = Depends(get_user_rating_service)
):
    service.delete_all_ratings()
import logging
from fastapi import APIRouter
from sqlalchemy.orm import Session
from db import get_db
from fastapi import Depends

from model.DTOs.UserDTO import UserCreate, UserOut, UserUpdate
from service.UserService import UserService
from service.AchievementService import AchievementService
from model.DTOs.AchievementDTO import UserAchievementOut, AchievementStatusOut
from dependencies import get_user_service, get_achievement_service

router = APIRouter(tags=["User methods"])

@router.get("/users/{id}", response_model=UserOut)
async def get_user(id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(id)

@router.post("/users", response_model=UserOut)
async def create_user(dto: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(dto)

@router.put("/users/{id}", response_model=UserOut)
async def update_user(id: int, dto: UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update_user(id, dto)

@router.delete("/users/{id}", response_model=None)
async def delete_user(id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(id)

@router.get("/users", response_model=list[UserOut])
async def get_users(service: UserService = Depends(get_user_service)) -> list[UserOut]:
    return service.get_all_users()
    
@router.delete("/users", response_model=None)
async def delete_all_users(service: UserService = Depends(get_user_service)) -> None:
    service.delete_all_users()

@router.get("/users/{id}/achievements", response_model=list[UserAchievementOut])
async def get_user_achievements(id: int, service: AchievementService = Depends(get_achievement_service)):
    return service.get_user_achievements(id)

@router.get("/users/{id}/achievements/status", response_model=list[AchievementStatusOut])
async def get_achievements_status(id: int, service: AchievementService = Depends(get_achievement_service)):
    return service.get_achievements_status(id)

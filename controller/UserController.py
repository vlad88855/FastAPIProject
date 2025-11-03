from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db

from model.DTOs.UserDTO import UserCreate, UserOut, UserUpdate
from model.User import User
from repository.UserRepository import UserRepository
from service import UserService
from service.UserService import UserService

router = APIRouter()

@router.get("/users/{id}", response_model=UserOut)
async def get_user(id: int):
    return UserService.get_user(id)

@router.post("/users", response_model=UserOut)
async def create_user(dto: UserCreate):
    return UserService.create_user(dto.username, dto.email, dto.password)

@router.put("/users/{id}", response_model=UserOut)
async def update_user(id: int, dto: UserUpdate):
    return UserService.update_user(id, dto.username, dto.email, dto.password)

@router.delete("/users/{id}", response_model=UserOut)
async def delete_user(id: int):
    return UserService.delete_user(id)

@router.get("/users", response_model=UserOut)
async def get_users() -> list[UserOut]:
    return UserService.get_all_users()
@router.delete("/users", response_model=UserOut)
async def delete_all_users() -> None:
    UserRepository.delete_all_users()

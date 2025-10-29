from fastapi import APIRouter

from model.User import User
from repository.UserRepository import UserRepository
from service import UserService
from service.UserService import UserService

router = APIRouter()

@router.get("/users/{id}")
async def get_user(id: int):
    return UserService.get_user(id)

@router.post("/users")
async def create_user(username: str, email: str, password: str):
    return UserService.create_user(username, email, password)

@router.put("/users/{id}")
async def update_user(id: int, username: str, email: str, password: str):
    return UserService.update_user(id, username, email, password)

@router.delete("/users/{id}")
async def delete_user(id: int):
    return UserService.delete_user(id)

@router.get("/users")
async def get_users():
    return UserService.get_all_users()
@router.delete("/users")
async def delete_all_users():
    UserRepository.delete_all_users()

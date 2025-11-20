from fastapi import APIRouter
from sqlalchemy.orm import Session
from db import get_db
from fastapi import Depends

from model.DTOs.UserDTO import UserCreate, UserOut, UserUpdate
from repository.UserRepository import UserRepository
from service.UserService import UserService

router = APIRouter(tags=["User methods"])

@router.get("/users/{id}", response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db=db))
    return service.get_user(id)

@router.post("/users", response_model=UserOut)
async def create_user(dto: UserCreate, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db=db))
    return service.create_user(dto)

@router.put("/users/{id}", response_model=UserOut)
async def update_user(id: int, dto: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db=db))
    return service.update_user(id, dto)

@router.delete("/users/{id}", response_model=None)
async def delete_user(id: int, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db=db))
    return service.delete_user(id)

@router.get("/users", response_model=list[UserOut])
async def get_users(db: Session = Depends(get_db)) -> list[UserOut]:
    service = UserService(UserRepository(db=db))
    return service.get_all_users()
    
@router.delete("/users", response_model=None)
async def delete_all_users(db: Session = Depends(get_db)) -> None:
    service = UserService(UserRepository(db=db))
    service.delete_all_users()

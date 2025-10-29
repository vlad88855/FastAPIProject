from pydantic import EmailStr

from model.User import User
from repository import UserRepository
from repository.UserRepository import UserRepository


class UserService():

    @classmethod
    def create_user(cls, username: str, email: EmailStr, password: str) -> User:
        return UserRepository.create_user(username, email, password)

    @classmethod
    def delete_user(cls, id: int):
        return UserRepository.delete_user(id)

    @classmethod
    def get_user(cls, id: int) -> User:
        return UserRepository.get_user(id)
    @classmethod
    def get_all_users(cls) -> dict:
        return UserRepository.get_all_users()

    @classmethod
    def update_user(cls, id: int, username: str, email: str, password: str) -> User:
        return UserRepository.update_user(id, username, email, password)
    @classmethod
    def delete_all_movies(cls):
        UserRepository.delete_all_users()


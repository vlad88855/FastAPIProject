from model.UserORM import UserORM
from model.DTOs.UserDTO import UserCreate, UserOut, UserUpdate
from repository.UserRepository import UserRepository

class UserService():

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, dto: UserCreate) -> UserOut:
        user = self.repository.create_user(dto)
        return UserOut.model_validate(user)

    def delete_user(self, id: int):
        return self.repository.delete_user(id)

    def get_user(self, id: int) -> UserOut:
        user = self.repository.get_user(id)
        return UserOut.model_validate(user)

    def get_all_users(self) -> list[UserOut]:
        users = self.repository.get_all_users()
        return [UserOut.model_validate(user) for user in users]

    def update_user(self, id: int, dto: UserUpdate) -> UserOut:
        user = self.repository.update_user(id, dto)
        return UserOut.model_validate(user)

    def delete_all_users(self):
        return self.repository.delete_all_users()
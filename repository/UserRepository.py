from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from model.DTOs.UserDTO import UserCreate, UserUpdate
from model.UserORM import UserORM
from repository.exceptions import EmailExistsException, UsernameExistsException, UserNotFoundException


class UserRepository():
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, dto: UserCreate) -> UserORM:
        try:
            user = UserORM(username=dto.username, email=dto.email, password=dto.password)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            msg = str(e.orig).lower()
            if "uq_users_username" in msg or "username" in msg:
                raise UsernameExistsException(f"Username {dto.username} already exists")
            if "uq_users_email" in msg or "email" in msg:
                raise EmailExistsException(f"Email {dto.email} already exists")
            raise

    def delete_user(self, id: int):
        try:
            user = self.get_user(id)
            self.db.delete(user)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise e

    def get_user(self, id: int) -> UserORM:
        user = self.db.get(UserORM, id)
        if not user:
            raise UserNotFoundException(f"User {id} not found")
        return user

    def get_all_users(self) -> list[UserORM]:
        users = self.db.query(UserORM).all()
        return users

    def update_user(self, id: int, dto: UserUpdate) -> UserORM:
        user = self.get_user(id)
        if dto.username is not None:
            user.username = dto.username
        if dto.email is not None:
            user.email = dto.email
        if dto.password is not None:
            user.password = dto.password
        try:
            self.db.commit()
        except IntegrityError as ex:
            self.db.rollback()
            msg = str(ex.orig).lower()
            if "uq_users_username" in msg or "username" in msg:
                raise UsernameExistsException(f"Username {dto.username} already exists")
            if "uq_users_email" in msg or "email" in msg:
                raise EmailExistsException(f"Email {dto.email} already exists")
            raise
        self.db.refresh(user)
        return user
    def delete_all_users(self) -> None:
        try:
            self.db.query(UserORM).delete()
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise e
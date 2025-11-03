from pydantic import EmailStr

from model.User import User
from repository.exceptions import EmailExistsException, UsernameExistsException, UserNotFoundException


class UserRepository():
    _user_id_counter: int = 0
    _users = {}


    @classmethod
    def get_usernames(cls) -> list[str]:
        return [val.username for val in cls._users.values()]
    @classmethod
    def get_emails(cls) -> list[EmailStr]:
        return [val.email for val in cls._users.values()]

    @classmethod
    def create_user(cls, dto: UserCreate) -> User:
        if dto.username in cls.get_usernames():
            raise UsernameExistsException(f"Username {dto.username} already exists")
        if dto.email in cls.get_emails():
            raise EmailExistsException(f"Email {dto.email} already exists")
            
        cls._user_id_counter += 1

        user = User(id=cls._user_id_counter, **dto.model_dump())
        cls._users[user.id] = user
        return user

    @classmethod
    def delete_user(cls, id: int):
        user = cls._users.get(id)
        if not user:
            raise UserNotFoundException(f"Username {id} does not exist")
        cls._users.pop(id)

    @classmethod
    def get_user(cls, id: int) -> User:
        user = cls._users.get(id)
        if not user:
            raise UserNotFoundException(f"Username {id} does not exist")
        return user

    @classmethod
    def get_all_users(cls) -> list[User]:
        return list(cls._users.values())

    @classmethod
    def update_user(cls, id: int, dto: UserUpdate) -> User:
        user = cls.get_user(id)
        new_username = dto.username.lower()
        new_email = dto.email.lower()

        for other_user in cls.get_all_users():
            if other_user.id == user.id:
                continue
            if other_user.username.lower() == new_username:
                raise UsernameExistsException(f"Username {new_username} already exists")
            if other_user.email.lower() == new_email:
                raise EmailExistsException(f"Email {dto.email} already exists")

        user.email = dto.email
        user.username = dto.username
        user.password = dto.password
        return user

    @classmethod
    def delete_all_users(cls):
        cls._users.clear()
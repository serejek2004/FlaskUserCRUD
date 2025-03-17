import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.user.dao import UserDAO
from app.user.model import User


def is_valid_email(email):
    return re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email)


class UserService:
    def __init__(self, db: SQLAlchemy):
        self.dao = UserDAO(db)

    def register(self, new_user: User) -> tuple[None, int] | tuple[User, int]:

        user_from_db = self.dao.get_user_by_email(new_user.email)
        if not is_valid_email(new_user.email) \
                or len(new_user.username) > 80 \
                or len(new_user.email) > 80 \
                or user_from_db:
            return None, 409

        user_to_create = User(username=new_user.username,
                              email=new_user.email)

        new_user = self.dao.register(user_to_create)

        return new_user.to_dict(), 201

    def get_users_by_username(self, username: str) -> list:
        users = self.dao.get_users_by_username(username)

        return [user.to_dict() for user in users]

    def get_user_by_email(self, email: str) -> dict:
        user = self.dao.get_user_by_email(email)

        return user.to_dict()

    def get_users_by_date_registration(self, start_date: datetime, end_date: datetime) -> list:
        users = self.dao.get_users_by_date_registration(start_date, end_date)

        return [user.to_dict() for user in users]

    def get_users_by_username_and_by_date_registration(self, username: str,
                                                       start_date: datetime,
                                                       end_date: datetime) -> list:
        users = self.dao.get_users_by_username_and_by_date_registration(username, start_date, end_date)

        return [user.to_dict() for user in users]

    def get_all(self) -> list:
        users = self.dao.get_all()

        return [user.to_dict() for user in users]

    def delete_user_by_email(self, email: str) -> bool:
        user = self.dao.get_user_by_email(email)

        if user:
            self.dao.delete_user_by_email(email)
            return True
        else:
            return False

    def update_user_by_email(self, email: str, user_dto: User) -> tuple[dict, int] | tuple[None, int]:
        user = self.dao.get_user_by_email(email)

        if user_dto.email and user_dto.email != email:
            if self.dao.get_user_by_email(user_dto.email):
                return None, 400

        if user:
            user = self.dao.update_user(email, user_dto)
            return user.to_dict(), 200
        else:
            return None, 404

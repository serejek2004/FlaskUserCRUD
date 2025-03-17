from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from app.user.model import User


class UserDAO:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def register(self, user: User) -> User:
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def get_users_by_username(self, username: str) -> list:
        return self.db.session.query(User).filter_by(username=username)

    def get_user_by_email(self, email: str) -> User:
        return self.db.session.query(User).filter_by(email=email).first()

    def get_users_by_date_registration(self, start_time: datetime, end_time: datetime):
        return self.db.session.query(User).filter(and_(User.created_at > start_time, User.created_at < end_time)).all()

    def get_users_by_username_and_by_date_registration(self, username: str, start_time: datetime, end_time: datetime):
        return self.db.session.query(User).filter(and_(User.created_at > start_time,
                                                       User.created_at < end_time,
                                                       or_(User.username.like(f"%{username}%")))).all()

    def get_all(self) -> list:
        return self.db.session.query(User).all()

    def delete_user_by_email(self, email):
        self.db.session.query(User).filter_by(email=email).delete()
        self.db.session.commit()

    def update_user(self, email: str, user_dto: User) -> User:
        user = self.db.session.query(User).filter_by(email=email).first()

        user.username = user_dto.username
        user.email = user_dto.email

        self.db.session.commit()

        return user

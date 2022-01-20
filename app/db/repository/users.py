from typing import Optional

from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserUpdate
from app.db.models import User
from app.core.hashing import Hasher


class UserRepository:
    @staticmethod
    def retrieve_user_by_id(id: int, db: Session):
        """
        Get a specific user using by id
        :param id:
        :param db:
        :return:
        """
        user = db.query(User).filter(User.id == id).first()
        return user


    @staticmethod
    def retrieve_user_by_email(email: str, db: Session):
        """
        Get a specific user by email
        :param email:
        :param db:
        :return:
        """
        user = db.query(User).filter(User.email == email).first()
        return user


    @staticmethod
    def list_users(db: Session, limit: int = 10, skip: int = 0, search_email_phrase: Optional[str] = ""):
        """
        Get all users using the search_email_phrase
        :param db:
        :param search_email_phrase:
        :param limit:
        :param skip:
        :return:
        """
        users = db.query(User).filter(User.email.contains(search_email_phrase)).limit(limit).offset(skip).all()
        return users


    @staticmethod
    def create_new_user(user: UserCreate, db: Session, is_active: bool = True, is_superuser: bool = False):
        """
        Creates a new user in the database
        :param is_superuser:
        :param is_active:
        :param user:
        :param db:
        :return:
        """
        user = User(
            email=user.email,
            password=Hasher.get_password_hash(user.password),
            is_active=is_active,
            is_superuser=is_superuser
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    @staticmethod
    def update_user_by_id(id: int, user: dict, db: Session):
        """
        Update a user
        :param id:
        :param user:
        :param db:
        :return:
        """
        user_query = db.query(User).filter(User.id == id)
        # user not found
        if not user_query.first():
            return False

        user_query.update(user, synchronize_session=False)
        db.commit()
        return user_query.first()


    @classmethod
    def deactivate_user_by_id(cls, id: int, db: Session, new_user_active_status: bool = False):
        """
        Deactivates a user
        :param new_user_active_status:
        :param id:
        :param db:
        :return:
        """
        # check if user exists
        user = cls.retrieve_user_by_id(id, db)

        # user not found
        if not user:
            return False

        # change user active status to inactive
        user.is_active = new_user_active_status

        # update user
        return cls.update_user_by_id(id=id, user=user.to_json(), db=db)

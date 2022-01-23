from sqlalchemy.orm import Session

from ..models import User
from ..repository.user import UserRepository
from app.core.hashing import Hasher


class AuthRepository:
    @staticmethod
    def verify_credential(email, password, db: Session):
        """
        Verify user credential
        :param username:
        :param password:
        :param db:
        :return:
        """
        user = UserRepository.retrieve_user_by_email(email=email, db=db)

        # user not found or password doesn't match
        if not user or not Hasher.verify_password(password, user.password):
            return False
        return user


    @staticmethod
    def verify_user_isactive(user: User) -> object:
        """
        Verify user is active
        :param user:
        :return:
        """
        # user has been deactivated
        if not user.is_active:
            return False
        return user

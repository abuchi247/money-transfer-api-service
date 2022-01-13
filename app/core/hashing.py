from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify if plain_password matches hashed_password
        :param plain_password:
        :param hashed_password:
        :return: True if they match otherwise false
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(plain_password):
        """
        Generate a hash password for the plain_password
        :param plain_password:
        :return:
        """
        return pwd_context.hash(plain_password)
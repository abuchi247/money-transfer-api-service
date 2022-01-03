from pydantic import BaseSettings


# setting used to validate the environment variable for our application
class Settings(BaseSettings):
    # database
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # import from the .env file
    class Config:
        env_file = ".env"


settings = Settings()
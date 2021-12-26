from pydantic import BaseSettings

# settings from environment variables
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
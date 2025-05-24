from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MYSQL_USER: str
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str
    MYSQL_DB: str

    class Config:
        env_file = ".env"

settings = Settings()


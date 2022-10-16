from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm : str
    mongo_uri : str
    access_token_expire_minutes: int
    db_name: str
    class Config:
        env_file = ".env"

settings = Settings()

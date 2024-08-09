from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    app_name: str
    database_url: str

    class Config:
        env_file = ".env"


load_dotenv()
settings = Settings()
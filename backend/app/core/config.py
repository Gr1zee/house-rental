from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "House Rental"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./rental.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
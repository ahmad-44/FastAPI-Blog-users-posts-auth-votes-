from pydantic_settings import BaseSettings

# Load environment variables from .env file
class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: str
    database_name: str
    database_username: str 
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

# Instantiate settings to access environment variables
settings = Settings() 
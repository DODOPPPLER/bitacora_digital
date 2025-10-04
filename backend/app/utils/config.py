from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    db_host: str
    db_user: str
    db_pass: str
    db_name: str
    db_port: int 

    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LMSTUDIO_BASE_URL: str
    LMSTUDIO_API_KEY: str
    LMSTUDIO_MODEL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()


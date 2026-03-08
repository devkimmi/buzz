from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

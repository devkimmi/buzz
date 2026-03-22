from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gcp_project_id: str = "project-b2cde9a3-9ba7-4b13-91c"
    gcp_location: str = "us-central1"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

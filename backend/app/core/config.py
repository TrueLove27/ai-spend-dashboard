from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Spend Dashboard API"
    api_prefix: str = "/api/v1"
    data_dir: str = "data"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    usd_to_inr: float = 83.5
    scheduler_enabled: bool = True


settings = Settings()

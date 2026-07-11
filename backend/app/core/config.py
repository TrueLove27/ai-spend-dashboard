from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Cloud Spend Dashboard API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./spend_dashboard.db"
    cors_origins: list[str] = ["http://localhost:5174", "http://127.0.0.1:5174"]
    scheduler_enabled: bool = True

    # Live integrations (no key required for Frankfurter)
    frankfurter_base_url: str = "https://api.frankfurter.dev/v1"
    display_currency: str = "EUR"

    # Optional — add your Stripe TEST secret key to .env for live billing sync
    stripe_secret_key: str = ""
    stripe_enabled: bool = False


settings = Settings()
if settings.stripe_secret_key:
    settings.stripe_enabled = True

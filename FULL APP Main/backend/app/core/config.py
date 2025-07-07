from pydantic_settings import BaseSettings, SettingsConfigDict

# Define application settings using Pydantic-Settings
class Settings(BaseSettings):
    # Database connection URL
    DATABASE_URL: str

    # JWT (JSON Web Token) secret key for authentication
    SECRET_KEY: str
    # Algorithm used for JWT encoding/decoding
    ALGORITHM: str = "HS256"
    # Access token expiration time in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Model configuration for loading settings from .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Create a singleton instance of settings
settings = Settings()

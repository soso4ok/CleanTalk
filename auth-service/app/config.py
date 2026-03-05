from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/auth_db"

    model_config = {"env_prefix": "AUTH_", "env_file": ".env", "extra": "ignore"}


# Allow DATABASE_URL without prefix as well
class _Fallback(BaseSettings):
    AUTH_DATABASE_URL: str = ""
    SECRET_KEY: str = "change-me-in-production"
    model_config = {"env_file": ".env", "extra": "ignore"}


_fb = _Fallback()
settings = Settings(
    DATABASE_URL=_fb.AUTH_DATABASE_URL or Settings().DATABASE_URL,
    SECRET_KEY=_fb.SECRET_KEY,
)

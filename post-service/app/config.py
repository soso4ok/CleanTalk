from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/post_db"

    model_config = {"env_prefix": "POST_", "env_file": ".env", "extra": "ignore"}


class _Fallback(BaseSettings):
    POST_DATABASE_URL: str = ""
    SECRET_KEY: str = "change-me-in-production"
    model_config = {"env_file": ".env", "extra": "ignore"}


_fb = _Fallback()
settings = Settings(
    DATABASE_URL=_fb.POST_DATABASE_URL or Settings().DATABASE_URL,
    SECRET_KEY=_fb.SECRET_KEY,
)

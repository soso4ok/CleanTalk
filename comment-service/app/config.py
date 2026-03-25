from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/comment_db"
class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/comment_db"
    AI_BACKEND: str = "mock"  # gemini | huggingface | mock
    GEMINI_API_KEY: str = ""
    HF_MODEL_NAME: str = "martin-ha/toxic-comment-model"

    model_config = {"env_prefix": "COMMENT_", "env_file": ".env", "extra": "ignore"}


class _Fallback(BaseSettings):
    COMMENT_DATABASE_URL: str = ""
    SECRET_KEY: str = "change-me-in-production"
    AI_BACKEND: str = "mock"
    GEMINI_API_KEY: str = ""
    HF_MODEL_NAME: str = "martin-ha/toxic-comment-model"
    model_config = {"env_file": ".env", "extra": "ignore"}


_fb = _Fallback()
settings = Settings(
    DATABASE_URL=_fb.COMMENT_DATABASE_URL or Settings().DATABASE_URL,
    SECRET_KEY=_fb.SECRET_KEY,
    AI_BACKEND=_fb.AI_BACKEND,
    GEMINI_API_KEY=_fb.GEMINI_API_KEY,
    HF_MODEL_NAME=_fb.HF_MODEL_NAME,
)

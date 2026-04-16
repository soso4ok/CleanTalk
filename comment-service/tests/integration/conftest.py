import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os

from app.main import app
from app.database import Base, get_db
from app.dependencies import get_current_user, TokenData

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def engine(postgres_container):
    url = postgres_container.get_connection_url()
    # Replace 'postgresql+psycopg2' if needed, though get_connection_url usually returns it
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    from sqlalchemy import text
    try:
        yield db
    finally:
        # Clean up tables between tests
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f"DELETE FROM {table.name}"))
        db.commit()
        db.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def mock_user():
    return TokenData(user_id="user_abc", username="integrator")

@pytest.fixture
def authenticated_client(client, mock_user):
    app.dependency_overrides[get_current_user] = lambda: mock_user
    return client

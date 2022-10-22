from app.config import env
from app.data import Base, get_db
from app.data.auth import user
from app.data.auth.user import User, UserCreate
from app.logic.auth.login import create_access_token
from app.main import app

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

TESTDB_NAME = f"{env.DB_NAME}_test"
TESTDB_URL = f"{env.DB_TYPE}://{env.DB_USER}:{env.DB_PASS}@{env.DB_HOST}:{env.DB_PORT}/{TESTDB_NAME}"

test_engine = create_engine(TESTDB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)  # type: ignore

AUTHORIZED_USER_ID = 1
DUMMY_USERS_DATA = [
    {
        "name": "Mahmudur Rahman",
        "email": "mahmud@jogaar.com",
        "password": "should_be_hashed",
    },
    {
        "name": "Syed Fateen Navid",
        "email": "fateen@jogaar.com",
        "password": "should_be_hashed",
    },
    {
        "name": "Zaed Bin Monir",
        "email": "zaed@jogaar.com",
        "password": "should_be_hashed",
    },
]


@fixture
def session():
    Base.metadata.drop_all(bind=test_engine)  # type: ignore
    Base.metadata.create_all(bind=test_engine)  # type: ignore

    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session: Session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@fixture
def dummy_users(client: TestClient) -> list[dict]:
    # most tests depend on the structure and contents of this list
    # and so changing anything may break them
    # TODO derive test parameters programmatically

    resp_data = []
    for dummy_user_data in DUMMY_USERS_DATA:
        resp = client.post("/users", json=dummy_user_data)

        assert resp.status_code == status.HTTP_201_CREATED

        merged = {**dummy_user_data, **resp.json()}

        resp_data.append(merged)

    return resp_data


@fixture
def token(dummy_users: list[dict]) -> str:
    return create_access_token({"user_id": AUTHORIZED_USER_ID})


@fixture
def authorized_client(client: TestClient, token: str) -> TestClient:
    client.headers["Authorization"] = f"Bearer {token}"

    return client

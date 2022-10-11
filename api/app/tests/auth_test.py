from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user() -> None:
    res = client.get(
        "/users",
        json={"name": "asdf", "email": "asdf@asdf.com", "password": "shouldbehashed"},
    )
    print(res.json())


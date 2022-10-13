from app.data.auth.user import UserRead
from app.tests.conftest import client, session, dummy_users  # ignore unused warnings

from fastapi import status
from fastapi.testclient import TestClient
from pytest import mark

from pprint import pp


# def test_dummy(client, dummy_users):

#     pp(dummy_users)


@mark.parametrize(
    "in_json,out_status",
    [
        (
            {
                "name": "Rafi Hassan Chowdhury",
                "email": "rafi@jogaar.com",
                "password": "should_be_hashed",
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "name": "Zaed Bin Monir",
                "email": "zaed@jogaar.com",
                "password": "should_be_hashed",
            },
            status.HTTP_409_CONFLICT,  # depends on dummy_users
        ),
    ],
)
def test_create_user(
    in_json: dict, out_status: int, dummy_users: list[dict], client: TestClient
) -> None:
    resp = client.post("/users", json=in_json)

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_201_CREATED:
        _ = UserRead(**resp.json())  # response validation


@mark.parametrize(
    "in_id,out_status",
    [(2, status.HTTP_200_OK), (420, status.HTTP_404_NOT_FOUND)],
)
def test_read_user(
    in_id: int, out_status: int, dummy_users: list[dict], client: TestClient
) -> None:

    resp = client.get(f"/users/{in_id}")

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_200_OK:
        _ = UserRead(**resp.json())  # response validation


@mark.parametrize(
    "in_limit,in_offset,in_len,out_status",
    [
        (5, 0, 3, status.HTTP_200_OK),
        (9, 4, 0, status.HTTP_200_OK),
    ],
)
def test_read_users(
    in_limit: int,
    in_offset: int,
    in_len: int,
    out_status: int,
    dummy_users: list[dict],
    client: TestClient,
) -> None:
    resp = client.get(f"/users?limit={in_limit}&offset={in_offset}")

    assert resp.status_code == out_status

    resp_data = resp.json()

    assert len(resp_data) == in_len

    if resp.status_code == status.HTTP_200_OK and len(resp_data) > 0:
        _ = UserRead(**resp.json()[0])  # response validation


@mark.parametrize(
    "in_id,in_json,out_status",
    [
        (1, {"about": "generic intro", "contact": "01696969420"}, status.HTTP_200_OK),
        (2, {"email": "zaed@jogaar.com"}, status.HTTP_409_CONFLICT),
        (420, {"name": "..."}, status.HTTP_404_NOT_FOUND),
    ],
)
def test_update_user(
    in_id: int,
    in_json: dict,
    out_status: int,
    dummy_users: list[dict],
    client: TestClient,
) -> None:
    resp = client.put(f"/users/{in_id}", json=in_json)

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_200_OK:
        resp_data = resp.json()
        _ = UserRead(**resp_data)  # response validation

        assert resp_data | in_json == resp_data  # verify changes


@mark.parametrize(
    "in_id,out_status",
    [(2, status.HTTP_204_NO_CONTENT), (420, status.HTTP_404_NOT_FOUND)],
)
def test_delete_user(
    in_id: int, out_status: int, dummy_users: list[dict], client: TestClient
) -> None:
    resp = client.delete(f"/users/{in_id}")

    assert resp.status_code == out_status

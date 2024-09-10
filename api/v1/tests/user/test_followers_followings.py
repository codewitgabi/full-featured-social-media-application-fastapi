import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..    /../../../"))
)

from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session

client = TestClient(app)


def test_followers(
    mock_db_session: Session, access_token, current_user, mock_followers
):

    response = client.get(
        "/api/v1/users/hhh/followers",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Followers successfully returned"
    assert response.json()["data"] == [
        {"id": "hhh", "username": "joshua", "profile_picture": "hhh"},
        {"id": "jjj", "username": "joseph", "profile_picture": "jjj"},
    ]


def test_followings(
    mock_db_session: Session, access_token, current_user, mock_followings
):

    response = client.get(
        "/api/v1/users/jjj/followings",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Followings list successfully returned"
    assert response.json()["data"] == [
        {"id": "hhh", "username": "joshua", "profile_picture": "hhh"},
        {"id": "jjj", "username": "joseph", "profile_picture": "jjj"},
    ]

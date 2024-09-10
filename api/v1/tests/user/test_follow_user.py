import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..    /../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "/api/v1/users/jjj/follow"


def test_follow_user(
    mock_db_session: Session,
    current_user,
    access_token,
    mock_follow_user,
):

    response = client.patch(
        endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User followed successfully"


def test_unfollow_user(
    mock_db_session: Session, current_user, access_token, mock_unfollow_user
):

    response = client.delete(
        "/api/v1/users/jjj/unfollow",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User unfollowed successfully"

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/posts/xx-yy-zz"


def test_delete_post_success(
    mock_db_session: Session, access_token, current_user, mock_create_post
):
    response = client.delete(
        endpoint, headers={"authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 204
    assert response.json()["status_code"] == 204
    assert response.json()["message"] == "Post deleted successfully"


def test_delete_post_not_found(
    mock_db_session: Session, access_token, current_user, mock_delete_post_side_effect
):
    response = client.delete(
        endpoint, headers={"authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json()["status_code"] == 404
    assert response.json()["message"] == "Post not found"


def test_create_post_unauthenticated_user(
    mock_db_session: Session,
):
    response = client.delete(endpoint)

    assert response.status_code == 401

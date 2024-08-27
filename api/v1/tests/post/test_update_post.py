import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/posts/post-id"


def test_update_post_success(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_update_post,
):
    response = client.patch(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json={"content": "Update post content"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status_code"] == 200
    assert data["message"] == "Post updated successfully"
    assert data["data"] == {
        "user_id": "02bb30ec-c793-463f-a2ea-d83edd156628",
        "video": None,
        "id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
        "image": None,
        "content": "Update post content",
    }


def test_update_post_no_request_body(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_update_post_no_body_side_effect,
):
    response = client.patch(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json={},
    )

    data = response.json()

    assert response.status_code == 400
    assert data["status_code"] == 400
    assert data["message"] == "Please provide one of content, image or video"


def test_update_post_not_found(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_update_post_not_found_side_effect,
):
    response = client.patch(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json={"content": "Update post content"},
    )

    data = response.json()

    assert response.status_code == 404
    assert data["status_code"] == 404
    assert data["message"] == "Post not found"

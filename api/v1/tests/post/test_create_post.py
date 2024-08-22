import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/posts"


def test_create_post_success(
    mock_db_session: Session, access_token, current_user, mock_create_post
):
    response = client.post(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json={"content": "Test post content"},
    )

    assert response.status_code == 201
    assert response.json()["status_code"] == 201
    assert response.json()["data"] == {
        "user_id": "02bb30ec-c793-463f-a2ea-d83edd156628",
        "video": None,
        "id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
        "image": None,
        "content": "Lorem ipsum dolor sit amet.",
        "updated_at": "2024-08-22T23:59:25.816336+01:00",
        "created_at": "2024-08-22T23:59:25.816336+01:00",
    }


def test_create_post_invalid_content(
    mock_db_session: Session,
    access_token,
    current_user,
):
    response = client.post(
        endpoint, headers={"authorization": f"Bearer {access_token}"}, json={}
    )

    assert response.status_code == 400
    assert response.json()["status_code"] == 400
    assert response.json()["message"] == "Please provide one of content, image or video"


def test_create_post_unauthenticated_user(
    mock_db_session: Session,
):
    response = client.post(endpoint, json={})

    assert response.status_code == 401

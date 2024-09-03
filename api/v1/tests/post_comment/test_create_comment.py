import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)


import pytest
from main import app
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

client = TestClient(app)

endpoint = "api/v1/posts/ac3d6659-8f67-4a67-b690-9f77fab7e6e3/comments"


def test_create_comment_success(
    mock_db_session: Session, access_token, current_user, mock_create_comment
):

    response = client.post(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json={"comment": "Test comment"},
    )

    assert response.status_code == 201
    assert response.json()["status_code"] == 201
    assert response.json()["data"] == {
        "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
        "comment": "This is a very nice post",
        "created_at": "2024-08-22T23:59:25.816336+01:00",
        "updated_at": "2024-08-22T23:59:25.816336+01:00",
        "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
        "user": {
            "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
            "username": "izzyjosh",
            "profile_picture": {
                "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                "image": "user/profile_picture.img",
            },
        },
    }


def test_create_comment_invalid_content(
    mock_db_session: Session, access_token, current_user
):

    response = client.post(
        endpoint, headers={"authorization": f"Bearer {access_token}"}, json={}
    )

    assert response.status_code == 400
    assert response.json()["status_code"] == 400
    assert response.json()["message"] == "The comment cannot be an empty field"


def test_create_comment_unautthenticated_user(mock_db_session: Session):

    response = client.post(endpoint, json={})

    assert response.status_code == 401


def test_create_comment_post_not_found(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_create_comment_post_not_found_side_effect,
):

    response = client.post(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json={"comment": "Test comment"},
    )

    data = response.json()

    assert response.status_code == 404
    assert data["status_code"] == 404
    assert data["message"] == "Post not found"

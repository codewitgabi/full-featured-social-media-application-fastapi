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


def test_get_comments_success(
    mock_db_session: Session, current_user, access_token, mock_get_comments
):

    response = client.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert response.json()["message"] == "Comments successfully returned"
    assert response.json()["data"] == [
        {
            "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
            "comment": "This is a very nice post",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-23T11:59:25.816336+01:00",
            "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
            "user": {
                "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
                "username": "izzyjosh",
                "profile_picture": {
                    "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                    "image": "user/profile_picture.img",
                },
            },
        },
        {
            "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
            "comment": "This is a very nice post",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-23T11:59:25.816336+01:00",
            "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
            "user": {
                "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
                "username": "izzyjosh",
                "profile_picture": {
                    "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                    "image": "user/profile_picture.img",
                },
            },
        },
    ]

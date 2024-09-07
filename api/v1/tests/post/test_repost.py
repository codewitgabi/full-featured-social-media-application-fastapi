import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

import pytest
from main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


client = TestClient(app)
endpoint = "api/v1/posts/ggg/repost"


def test_repost(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_repost,
):

    response = client.post(
        endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "Test repost"},
    )

    assert response.status_code == 201
    assert response.json()["status_code"] == 201
    assert response.json()["message"] == "Reposted successfully"
    assert response.json()["data"] == {
        "user_id": "zzz",
        "post_id": "hhh",
        "content": "Test repost",
        "created_at": "2024-08-22T23:59:25.816336+01:00",
        "updated_at": "2024-08-22T23:59:25.816336+01:00",
        "repost_owner": {"id": "jjj", "image": "/picture", "username": "joshua"},
        "original_post": {
            "id": "kkk",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-22T23:59:25.816336+01:00",
            "content": "Tgis is the original post",
            "video": "null",
            "images": "null",
            "original_post_owner": {
                "id": "iii",
                "image": "/picture",
                "username": "joseph",
            },
        },
    }

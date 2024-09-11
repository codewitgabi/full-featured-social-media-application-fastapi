import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/posts"


def test_get_feeds(
        mock_db_session: Session,
        current_user,
        access_token,
        mock_get_feeds,):

    response = client.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["message"] == "Feeds returned successfully"
    assert response.json()["data"] == {
            "id": "jjj",
            "content":" this is a test post",
            "image": "null",
            "video": "null",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-22T23:59:25.816336+01:00",
            "post_owner": {
                "id": "kkk",
                "profile_picture": "null",
                "username": "izzyjosh",
                },
            "original_post": "null"
            }


def test_web_socket():
    
    with client.websocket_connect("/api/v1/posts/ws") as websocket:

        response = websocket.receive_text()
        assert response == "connected"

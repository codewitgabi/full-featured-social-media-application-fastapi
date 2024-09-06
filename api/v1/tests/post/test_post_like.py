import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/posts/dgdvdy38ixh/like"


def test_like_post(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_like_post,
):

    response = client.patch(
        endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_get_likes(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_get_post_likes,
):

    response = client.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert response.json()["data"] == {
        "user_id": "xxx",
        "post_id": "yyy",
        "liked": "True",
        "user": {"id": "jjj", "image": "hhh"},
    }

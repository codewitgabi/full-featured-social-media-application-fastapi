import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)


from main import app
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

client = TestClient(app)
endpoint = "/api/v1/notifications"


def test_get_notifications(
    mock_db_session: Session,
    current_user,
    access_token,
    mock_get_notifications,
):

    response = client.get(
        endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["data"] == [
        {
            "id": "hhh",
            "message": "test notification",
            "created_at": "today",
            "status": "unread",
        },
    ]

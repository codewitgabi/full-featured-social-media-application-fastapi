import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/users/12345"


def test_get_user_detail(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_user_detail,
):
    response = client.get(endpoint, headers={"authorization": f"Bearer {access_token}"})

    data = response.json()

    assert response.status_code == 200
    assert data["status_code"] == 200
    assert data["message"] == "User detail fetched successfully"
    assert data["data"] == {
        "id": "12345",
        "username": "test",
        "email": "test@test.com",
    }

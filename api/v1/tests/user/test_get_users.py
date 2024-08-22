import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/users"


def test_get_user_detail(mock_db_session: Session, mock_user_detail, mock_get_users):
    response = client.get(endpoint)

    data = response.json()

    assert response.status_code == 200
    assert data["status_code"] == 200
    assert data["message"] == "User list fetched successfully"
    assert data["data"] == [
        {"id": 1, "username": "codewitgabi"},
        {"id": 2, "username": "test"},
        {"id": 3, "username": "doe"},
    ]

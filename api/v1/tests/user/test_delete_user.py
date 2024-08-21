import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "api/v1/users/123"


def test_delete_user(
    mock_db_session: Session, access_token, current_user, mock_delete_user
):
    response = client.delete(
        endpoint, headers={"authorization": f"Bearer {access_token}"}
    )

    data = response.json()

    assert response.status_code == 204
    assert data["status_code"] == 204
    assert data["message"] == "User deleted successfully"


def test_delete_user_permission_denied(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_delete_user_effect,
):
    response = client.delete(
        endpoint, headers={"authorization": f"Bearer {access_token}"}
    )

    data = response.json()

    assert response.status_code == 403
    assert data["status_code"] == 403
    assert data["message"] == "You do not have permission to delete this user"

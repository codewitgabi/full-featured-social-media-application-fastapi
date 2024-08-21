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


def test_update_user_profile(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_user_update,
):
    body = {"bio": "Update my bio", "social_links": ["http://example.com"]}

    response = client.patch(
        endpoint, headers={"authorization": f"Bearer {access_token}"}, json=body
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status_code"] == 200
    assert data["message"] == "User profile updated successfully"
    assert data["data"] == {
        "id": "12345",
        "username": "test",
        "email": "test@test.com",
    }


def test_update_user_side_effect(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_user_update_effect,
):
    body = {"bio": "Update my bio", "social_links": ["http://example.com"]}

    response = client.patch(
        endpoint, headers={"authorization": f"Bearer {access_token}"}, json=body
    )

    data = response.json()

    assert response.status_code == 403
    assert data["status_code"] == 403
    assert data["message"] == "You do not have permission to update this profile"

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from api.v1.services.user import UserService
from main import app

client = TestClient(app)
endpoint = "api/v1/auth/login"
mock_id = str(uuid4())


def test_login_success(
    mock_db_session: Session,
    mock_user_service: UserService,
    override_handle_login: None,
):
    """Test for successful user login"""

    response = client.post(
        endpoint, json={"email": "test@example.com", "password": "12345"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "message": "User login successful",
        "data": {
            "access_token": "'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.KkiNWdzcAgD_0PF169pvBausbptBe1mSQcTorMEqciA",
            "user": {
                "id": "341df7fe-3d16-4c43-a0eb-5f7e2940d012",
                "username": "test",
                "email": "test@example.com",
                "role": "user",
            },
        },
    }


def test_incorrect_email(
    mock_db_session: Session,
    mock_user_service: UserService,
    mock_invalid_account_effect: None,
):
    """Test for incorrect email address"""

    response = client.post(
        endpoint, json={"email": "test@example.com", "password": "12345"}
    )

    assert response.status_code == 400
    assert response.json() == {
        "status_code": 400,
        "message": "No account associated with provided email",
    }


def test_incorrect_password(
    mock_db_session: Session,
    mock_user_service: UserService,
    mock_incorrect_password: None,
):
    """Test for incorrect password"""

    response = client.post(
        endpoint, json={"email": "test@example.com", "password": "12345"}
    )

    assert response.status_code == 400
    assert response.json() == {
        "status_code": 400,
        "message": "Incorrect password",
    }

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
endpoint = "api/v1/auth/register"
mock_id = str(uuid4())


def test_register_user_success(
    mock_db_session: Session, mock_user_service: UserService, override_create: None
):
    data = {
        "username": "testUser",
        "email": "testEmail@gmail.com",
        "password": "12345",
    }

    response = client.post("/api/v1/auth/register", json=data)

    assert response.status_code == 201
    assert response.json() == {
        "status_code": 201,
        "message": "User created successfully",
        "data": {
            "username": "testUser",
            "email": "testEmail@mail.com",
            "password": "12345",
        },
    }

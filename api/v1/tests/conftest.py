import os
import sys


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from fastapi import HTTPException, status
import pytest
from uuid import uuid4
from main import app
from unittest.mock import patch, MagicMock
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.models.user import User

mock_id = str(uuid4())


@pytest.fixture
def mock_db_session():
    with patch("api.v1.utils.dependencies.get_db", autospec=True):
        mock_db = MagicMock()
        app.dependency_overrides[get_db] = lambda: mock_db
        yield mock_db
    app.dependency_overrides = {}


@pytest.fixture
def mock_user_service():
    with patch("api.v1.services.user.user_service", autospec=True) as mock_service:
        yield mock_service


@pytest.fixture
def override_create():
    with patch(
        "api.v1.services.user.UserService.create_user", autospec=True
    ) as mock_create:
        user = {
            "username": "testUser",
            "email": "testEmail@mail.com",
            "password": "12345",
        }

        mock_create.return_value = user
        yield mock_create


@pytest.fixture
def mock_user_exists():
    with patch(
        "api.v1.services.user.UserService.create_user", autospec=True
    ) as mock_create:
        mock_create.side_effect = HTTPException(
            status.HTTP_400_BAD_REQUEST, "User with email already exists"
        )

        yield mock_create


@pytest.fixture
def override_handle_login():
    with patch("api.v1.services.user.UserService.handle_login") as handle_login:
        response = {
            "access_token": "'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.KkiNWdzcAgD_0PF169pvBausbptBe1mSQcTorMEqciA",
            "user": {
                "id": "341df7fe-3d16-4c43-a0eb-5f7e2940d012",
                "username": "test",
                "email": "test@example.com",
                "role": "user",
            },
        }

        handle_login.return_value = response
        yield handle_login


@pytest.fixture
def mock_invalid_account_effect():
    with patch("api.v1.services.user.UserService.handle_login") as handle_login:
        handle_login.side_effect = HTTPException(
            400, detail="No account associated with provided email"
        )

        yield handle_login


@pytest.fixture
def mock_incorrect_password():
    with patch(
        "api.v1.services.user.UserService.verify_password"
    ) as incorrect_password:
        incorrect_password.side_effect = HTTPException(400, "Incorrect password")

        yield incorrect_password


@pytest.fixture
def mock_access_token():
    with patch(
        "api.v1.services.user.UserService.generate_access_token"
    ) as access_token:
        access_token.return_value = "access_token"

        yield access_token


def override_deps():
    return User(
        id="5d35b5b3-4eb7-4ad4-8082-b9af0de42c44",
        username="test-user",
        email="test-user@example.com",
        role="user",
    )


@pytest.fixture
def override_get_current_user():
    with patch(
        "api.v1.services.user.UserService.get_current_user", autospec=True
    ) as current_user:
        current_user.return_value = User(
            id="5d35b5b3-4eb7-4ad4-8082-b9af0de42c44",
        )
        app.dependency_overrides[user_service.get_current_user] = current_user
        yield current_user

    app.dependency_overrides = {}


@pytest.fixture
def override_blacklist_token():
    with patch(
        "api.v1.services.user.user_service.blacklist_token"
    ) as blacklist_token:
        yield blacklist_token

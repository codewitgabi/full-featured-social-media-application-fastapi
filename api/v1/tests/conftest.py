import os
import sys


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

import pytest
from uuid import uuid4
from main import app
from unittest.mock import patch, MagicMock
from api.v1.utils.dependencies import get_db

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

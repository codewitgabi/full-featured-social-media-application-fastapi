from fastapi import HTTPException
import pytest
from unittest.mock import patch

from api.v1.models.user import User
from api.v1.services.user import user_service
from main import app


@pytest.fixture
def mock_user_detail():
    with patch("api.v1.services.user.user_service.get_user_detail") as user_detail:
        user_detail.return_value = {
            "id": "12345",
            "username": "test",
            "email": "test@test.com",
        }

        yield user_detail


@pytest.fixture
def mock_user_update():
    with patch(
        "api.v1.services.user.user_service.update_user_profile"
    ) as update_user_profile:
        update_user_profile.return_value = {
            "id": "12345",
            "username": "test",
            "email": "test@test.com",
        }

        yield update_user_profile


@pytest.fixture
def mock_user_update_effect():
    with patch(
        "api.v1.services.user.user_service.get_user_detail"
    ) as user_detail_effect:
        user_detail_effect.side_effect = HTTPException(
            403, "You do not have permission to update this profile"
        )

        yield user_detail_effect


@pytest.fixture
def mock_delete_user():
    with patch(
        "api.v1.services.user.user_service.delete_user_profile"
    ) as delete_user_profile:
        yield delete_user_profile


@pytest.fixture
def mock_delete_user_effect():
    with patch(
        "api.v1.services.user.user_service.delete_user_profile"
    ) as delete_user_profile:
        delete_user_profile.side_effect = HTTPException(403, "You do not have permission to delete this user")

        yield delete_user_profile

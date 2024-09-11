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
        delete_user_profile.side_effect = HTTPException(
            403, "You do not have permission to delete this user"
        )

        yield delete_user_profile


@pytest.fixture
def mock_get_users():
    with patch("api.v1.services.user.user_service.fetch_all") as fetch_users:
        fetch_users.return_value = [
            {"id": 1, "username": "codewitgabi"},
            {"id": 2, "username": "test"},
            {"id": 3, "username": "doe"},
        ]

        yield fetch_users


@pytest.fixture
def mock_follow_user():

    with patch("api.v1.services.user.user_service.follow_user") as follow_user:
        yield follow_user


@pytest.fixture
def mock_unfollow_user():
    with patch("api.v1.services.user.user_service.unfollow_user") as unfollow_user:
        yield unfollow_user


@pytest.fixture
def mock_followers():

    with patch("api.v1.services.user.user_service.followers") as followers:
        followers.return_value = [
            {"id": "hhh", "username": "joshua", "profile_picture": "hhh"},
            {"id": "jjj", "username": "joseph", "profile_picture": "jjj"},
        ]
        yield followers


@pytest.fixture
def mock_followings():
    with patch("api.v1.services.user.user_service.followings") as followings:

        followings.return_value = [
            {"id": "hhh", "username": "joshua", "profile_picture": "hhh"},
            {"id": "jjj", "username": "joseph", "profile_picture": "jjj"},
        ]
        yield followings

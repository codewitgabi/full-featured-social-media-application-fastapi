import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from unittest.mock import patch
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from api.v1.services.user import UserService, user_service
from api.v1.models.user import User
from main import app

client = TestClient(app)
endpoint = "api/v1/auth/logout"


def test_logout_success(
    mock_db_session: Session,
    mock_user_service: UserService,
    override_get_current_user: User,
    override_blacklist_token: None,
):
    pass


def test_logout_token_already_blacklisted():
    pass

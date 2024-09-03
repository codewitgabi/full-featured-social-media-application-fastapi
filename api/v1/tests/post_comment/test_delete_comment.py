import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)

endpoint = "api/v1/posts/ac3d6659-8f67-4a67-b690-9f77fab7e6e3/comments/ac3d6659-8f67-4a67-b690-9f77fab7e6e3"


def test_delete_comment(
    mock_db_session: Session, access_token, current_user, mock_create_comment
):

    response = client.delete(
        endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 204
    assert response.json()["status_code"] == 204
    assert response.json()["message"] == "Comment deleted successfully"


def test_delete_comment_comment_not_found_side_effect(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_delete_comment_comment_not_found_side_effect,
):

    response = client.delete(
        endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json()["status_code"] == 404
    assert response.json()["message"] == "comment not found"

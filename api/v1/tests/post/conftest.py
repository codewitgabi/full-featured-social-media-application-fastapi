import os
import sys


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from fastapi import HTTPException
import pytest
from uuid import uuid4
from unittest.mock import patch

mock_id = str(uuid4())


@pytest.fixture
def mock_create_post():
    with patch("api.v1.services.post.post_service.create") as create_post:
        create_post.return_value = {
            "user_id": "02bb30ec-c793-463f-a2ea-d83edd156628",
            "video": None,
            "id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
            "image": None,
            "content": "Lorem ipsum dolor sit amet.",
            "updated_at": "2024-08-22T23:59:25.816336+01:00",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
        }

        yield create_post


@pytest.fixture
def mock_delete_post_side_effect():
    with patch("api.v1.services.post.post_service.delete") as create_post_side_effect:
        create_post_side_effect.side_effect = HTTPException(404, "Post not found")

        yield create_post_side_effect

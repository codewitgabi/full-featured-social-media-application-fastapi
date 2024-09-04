import os
import sys


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from fastapi import HTTPException
from main import app
import pytest
from uuid import uuid4
from unittest.mock import patch

mock_id = str(uuid4())


@pytest.fixture
def mock_create_comment():
    with patch("api.v1.services.post_comment.comment_service.create") as create_comment:

        create_comment.return_value = {
            "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
            "comment": "This is a very nice post",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-22T23:59:25.816336+01:00",
            "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
            "user": {
                "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
                "username": "izzyjosh",
                "profile_picture": {
                    "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                    "image": "user/profile_picture.img",
                },
            },
        }

        yield create_comment


@pytest.fixture
def mock_create_comment_no_content_side_effect():
    with patch(
        "api.v1.services.post_comment.comment_service.create"
    ) as create_comment_side_effect:

        create_comment_side_effect.side_effect = HTTPException(
            400, "please provide a comment"
        )
        yield create_comment_side_effect


@pytest.fixture
def mock_create_comment_post_not_found_side_effect():
    with patch(
        "api.v1.services.post_comment.comment_service.create"
    ) as create_comment_post_not_found_side_effect:

        create_comment_post_not_found_side_effect.side_effect = HTTPException(
            404, "Post not found"
        )
        yield create_comment_post_not_found_side_effect


@pytest.fixture
def mock_update_comment():
    with patch("api.v1.services.post_comment.comment_service.update") as update_comment:

        update_comment.return_value = {
            "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
            "comment": "This is a very nice post",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-23T11:59:25.816336+01:00",
            "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
            "user": {
                "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
                "username": "izzyjosh",
                "profile_picture": {
                    "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                    "image": "user/profile_picture.img",
                },
            },
        }
        yield update_comment


@pytest.fixture
def mock_update_comment_post_not_found_side_effect():
    with patch(
        "api.v1.services.post_comment.comment_service.update"
    ) as comment_update_post_not_found:

        comment_update_post_not_found.side_effect = HTTPException(404, "Post not found")

        yield comment_update_post_not_found


@pytest.fixture
def mock_update_comment_no_content_side_effect():
    with patch(
        "api.v1.services.post_comment.comment_service.update"
    ) as comment_update_no_content:

        comment_update_no_content.side_effect = HTTPException(
            400, "Please provide comment content"
        )

        yield comment_update_no_content


@pytest.fixture
def mock_delete_comment_comment_not_found_side_effect():
    with patch(
        "api.v1.services.post_comment.comment_service.delete"
    ) as delete_comment_side_effect:

        delete_comment_side_effect.side_effect = HTTPException(404, "comment not found")

        yield delete_comment_side_effect


@pytest.fixture
def mock_get_comments():
    with patch(
        "api.v1.services.post_comment.comment_service.get_comments"
    ) as get_comments:

        get_comments.return_value = [
            {
                "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
                "comment": "This is a very nice post",
                "created_at": "2024-08-22T23:59:25.816336+01:00",
                "updated_at": "2024-08-23T11:59:25.816336+01:00",
                "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
                "user": {
                    "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
                    "username": "izzyjosh",
                    "profile_picture": {
                        "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                        "image": "user/profile_picture.img",
                    },
                },
            },
            {
                "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
                "comment": "This is a very nice post",
                "created_at": "2024-08-22T23:59:25.816336+01:00",
                "updated_at": "2024-08-23T11:59:25.816336+01:00",
                "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
                "user": {
                    "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
                    "username": "izzyjosh",
                    "profile_picture": {
                        "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                        "image": "user/profile_picture.img",
                    },
                },
            },
        ]

        yield get_comments

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


@pytest.fixture
def mock_update_post():
    with patch("api.v1.services.post.post_service.update") as update_post:
        update_post.return_value = {
            "user_id": "02bb30ec-c793-463f-a2ea-d83edd156628",
            "video": None,
            "id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
            "image": None,
            "content": "Update post content",
        }

        yield update_post


@pytest.fixture
def mock_update_post_no_body_side_effect():
    with patch("api.v1.services.post.post_service.update") as update_post_side_effect:
        update_post_side_effect.side_effect = HTTPException(
            400, "Please provide one of content, image or video"
        )

        yield update_post_side_effect


@pytest.fixture
def mock_update_post_not_found_side_effect():
    with patch("api.v1.services.post.post_service.update") as update_post_side_effect:
        update_post_side_effect.side_effect = HTTPException(404, "Post not found")

        yield update_post_side_effect


@pytest.fixture
def mock_like_post():
    with patch("api.v1.services.post.post_service.like_post") as like_post:
        like_post.return_value = {"message": "post liked successfully"}
        yield like_post


@pytest.fixture
def mock_get_post_likes():
    with patch("api.v1.services.post.post_service.get_likes") as post_likes:
        post_likes.return_value = {
            "user_id": "xxx",
            "post_id": "yyy",
            "liked": "True",
            "user": {"id": "jjj", "image": "hhh"},
        }

        yield post_likes


@pytest.fixture
def mock_repost():
    with patch("api.v1.services.post.post_service.repost") as repost:

        repost.return_value = {
            "user_id": "zzz",
            "post_id": "hhh",
            "content": "Test repost",
            "created_at": "2024-08-22T23:59:25.816336+01:00",
            "updated_at": "2024-08-22T23:59:25.816336+01:00",
            "repost_owner": {"id": "jjj", "image": "/picture", "username": "joshua"},
            "original_post": {
                "id": "kkk",
                "created_at": "2024-08-22T23:59:25.816336+01:00",
                "updated_at": "2024-08-22T23:59:25.816336+01:00",
                "content": "Tgis is the original post",
                "video": "null",
                "images": "null",
                "original_post_owner": {
                    "id": "iii",
                    "image": "/picture",
                    "username": "joseph",
                },
            },
        }

        yield repost


@pytest.fixture
def mock_get_feeds():
    with patch("api.v1.services.post.post_service.get_feeds") as get_feeds:

        get_feeds.return_value = {
                "id": "jjj",
                "content":" this is a test post",
                "image": "null",
                "video": "null",
                "created_at": "2024-08-22T23:59:25.816336+01:00",
                "updated_at": "2024-08-22T23:59:25.816336+01:00",
                "post_owner": {
                    "id": "kkk",
                    "profile_picture": "null",
                    "username": "izzyjosh",
                    },
                "original_post": "null"
                }
        yield get_feeds

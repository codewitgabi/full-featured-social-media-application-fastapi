import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

import pytest
import fastapi
from unittest.mock import patch


@pytest.fixture
def mock_get_notifications():
    with patch(
        "api.v1.services.notification.notification_service.notifications"
    ) as get_notifications:
        get_notifications.return_value = [
            {
                "id": "hhh",
                "message": "test notification",
                "created_at": "today",
                "status": "unread",
            },
        ]
        yield get_notifications

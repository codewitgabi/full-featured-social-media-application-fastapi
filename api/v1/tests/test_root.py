import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_server_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "message": "Welcome to fastapi-social-media-api",
    }


def test_404_not_found_error():
    response = client.get("/zzz")

    assert response.status_code == 404
    assert response.json() == {"status_code": 404, "message": "Not Found"}


def test_other_error_response():
    response = client.post("/")

    assert response.status_code == 405
    assert response.json() == {"status_code": 405, "message": "Method Not Allowed"}

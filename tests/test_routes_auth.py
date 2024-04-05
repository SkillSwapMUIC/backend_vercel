from unittest.mock import patch

import pytest

from app.db import db
from index import app


@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_login_success(test_client):
    with patch("app.controller.auth_controller.login_user") as mock_login_user:
        mock_login_user.return_value = (True, "dummy_token")

        response = test_client.post(
            "auth/login",
            json={
                "username": "test@example.com",
                "password": "password",
                "role": "teacher",
            },
        )
        assert response.status_code == 200
        assert "auth_token" in response.json


def test_login_invalid_credentials(test_client):
    with patch("app.controller.auth_controller.login_user") as mock_login_user:
        mock_login_user.return_value = (False, None)

        response = test_client.post(
            "auth/login",
            json={
                "username": "test@example.com",
                "password": "wrong_password",
                "role": "teacher",
            },
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json["error"]


def test_is_teacher_true(test_client):
    with patch("app.controller.auth_controller.is_teacher") as mock_is_teacher:
        mock_is_teacher.return_value = True

        response = test_client.post(
            "auth/is-teacher", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 200
        assert response.json["access_allowed"] == "True"


def test_is_teacher_false(test_client):
    with patch("app.controller.auth_controller.is_teacher") as mock_is_teacher:
        mock_is_teacher.return_value = False

        response = test_client.post(
            "auth/is-teacher", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 200
        assert response.json["access_allowed"] == "False"

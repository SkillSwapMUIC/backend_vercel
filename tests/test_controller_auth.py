from unittest.mock import MagicMock, patch

import pytest

from app import db
from app.controller.auth_controller import login_user
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


def test_login_user_new_user(test_client):
    email = "test@example.com"
    password = "password"
    role = "teacher"

    with app.app_context():
        with patch("app.controller.auth_controller.User.query.filter_by") as mock_query:
            mock_query.return_value.first.return_value = None

            success, auth_token = login_user(email, password, role)
            assert success


def test_login_user_existing_user_correct_password(test_client):
    email = "test@example.com"
    password = "password"
    role = "teacher"

    with app.app_context():
        with patch("app.controller.auth_controller.User.query.filter_by") as mock_query:
            mock_user_instance = MagicMock()
            mock_query.return_value.first.return_value = mock_user_instance

            success, auth_token = login_user(email, password, role)
            assert success


def test_login_user_existing_user_incorrect_password(test_client):
    email = "test@example.com"
    password = "incorrect_password"
    role = "teacher"

    with app.app_context():
        with patch("app.controller.auth_controller.User.query.filter_by") as mock_query:
            mock_user_instance = MagicMock()
            mock_user_instance.check_password.return_value = False
            mock_query.return_value.first.return_value = mock_user_instance

            success, auth_token = login_user(email, password, role)
            assert success
            #  because new account should be created

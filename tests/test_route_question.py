from unittest.mock import patch

import pytest
from sqlalchemy import exc

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


def test_submit_question_success(test_client):
    data = {"title": "Test Title", "content": "Test Content", "subject": "Test Subject"}
    response = test_client.post("/qanda/question/submit", json=data)
    assert response.status_code == 201
    assert response.json["title"] == data["title"]
    assert response.json["content"] == data["content"]
    assert response.json["subject"] == data["subject"]


def test_submit_question_missing_fields(test_client):
    data = {"content": "Test Content", "subject": "Test Subject"}
    response = test_client.post("/qanda/question/submit", json=data)
    assert response.status_code == 400
    assert "error" in response.json


def test_submit_question_integrity_error(test_client):
    # Mocking the post_question method to raise IntegrityError
    with patch(
        "app.controller.qanda_controller.post_question",
        side_effect=exc.IntegrityError("Integrity Error", None, None),
    ):
        data = {
            "title": "Test Title",
            "content": "Test Content",
            "subject": "Test Subject",
        }
        response = test_client.post("/qanda/question/submit", json=data)
        assert response.status_code == 400
        assert "Integrity error" in response.json["error"]


def test_submit_question_sqlalchemy_error(test_client):
    # Mocking the post_question method to raise SQLAlchemyError
    with patch(
        "app.controller.qanda_controller.post_question",
        side_effect=exc.SQLAlchemyError("SQLAlchemy Error"),
    ):
        data = {
            "title": "Test Title",
            "content": "Test Content",
            "subject": "Test Subject",
        }
        response = test_client.post("/qanda/question/submit", json=data)
        assert response.status_code == 500
        assert "SQLAlchemy error" in response.json["error"]


def test_submit_question_general_error(test_client):
    # Mocking the post_question method to raise a generic Exception
    with patch(
        "app.controller.qanda_controller.post_question",
        side_effect=Exception("Generic Error"),
    ):
        data = {
            "title": "Test Title",
            "content": "Test Content",
            "subject": "Test Subject",
        }
        response = test_client.post("/qanda/question/submit", json=data)
        assert response.status_code == 500
        assert "An error occurred" in response.json["error"]

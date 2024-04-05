from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

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


def test_answer_question_success(test_client):
    with patch(
        "app.controller.qanda_controller.answer_on_question"
    ) as mock_answer_on_question:
        mock_answer_on_question.return_value = None

        response = test_client.post(
            "qanda/answer-on/123",
            json={"content": "Sample answer", "auth_token": "dummy_token"},
        )
        assert response.status_code == 201
        assert "Answer submitted successfully" in response.json["message"]


def test_answer_question_database_error(test_client):
    with patch(
        "app.controller.qanda_controller.answer_on_question"
    ) as mock_answer_on_question:
        mock_answer_on_question.side_effect = SQLAlchemyError("Database Error")

        response = test_client.post(
            "qanda/answer-on/123",
            json={"content": "Sample answer", "auth_token": "dummy_token"},
        )
        assert response.status_code == 500
        assert "Database error" in response.json["error"]


def test_get_all_subjects_success(test_client):
    with patch(
        "app.controller.qanda_controller.get_all_subjects"
    ) as mock_get_all_subjects:
        mock_get_all_subjects.return_value = ["subject1", "subject2", "subject3"]

        response = test_client.get("qanda/all-subjects")
        assert response.status_code == 200
        assert response.json == ["subject1", "subject2", "subject3"]


def test_get_all_subjects_database_error(test_client):
    with patch(
        "app.controller.qanda_controller.get_all_subjects"
    ) as mock_get_all_subjects:
        mock_get_all_subjects.side_effect = SQLAlchemyError("Database Error")

        response = test_client.get("qanda/all-subjects")
        assert response.status_code == 500
        assert "Database error" in response.json["error"]


def test_delete_question_success(test_client):
    with patch("app.controller.qanda_controller.delete_post") as mock_delete_post:
        mock_delete_post.return_value = True

        response = test_client.post(
            "qanda/delete/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 200
        assert "Question deleted successfully" in response.json["message"]


def test_delete_question_not_found(test_client):
    with patch("app.controller.qanda_controller.delete_post") as mock_delete_post:
        mock_delete_post.return_value = False

        response = test_client.post(
            "qanda/delete/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 404
        assert "Question not found or user not authorized" in response.json["error"]


def test_delete_question_database_error(test_client):
    with patch("app.controller.qanda_controller.delete_post") as mock_delete_post:
        mock_delete_post.side_effect = SQLAlchemyError("Database Error")

        response = test_client.post(
            "qanda/delete/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 500
        assert "Database error" in response.json["error"]


def test_delete_question_general_error(test_client):
    with patch("app.controller.qanda_controller.delete_post") as mock_delete_post:
        mock_delete_post.side_effect = Exception("Generic Error")

        response = test_client.post(
            "qanda/delete/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 500
        assert "An error occurred" in response.json["error"]

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


def test_get_question_missing_auth_token(test_client):
    response = test_client.post("qanda/thread/byid/123")
    assert response.status_code == 500
    assert "An error occurred" in response.json["error"]


def test_get_question_missing_thread(test_client):
    with patch(
        "app.controller.qanda_controller.get_thread_by_id"
    ) as mock_get_thread_by_id:
        mock_get_thread_by_id.return_value = None

        response = test_client.post(
            "qanda/thread/byid/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 404
        assert "No thread found for the given question id" in response.json["error"]


def test_get_question_database_error(test_client):
    with patch(
        "app.controller.qanda_controller.get_thread_by_id"
    ) as mock_get_thread_by_id:
        mock_get_thread_by_id.side_effect = SQLAlchemyError("Database Error")

        response = test_client.post(
            "qanda/thread/byid/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 500
        assert "Database error" in response.json["error"]


def test_get_question_json_error(test_client):
    response = test_client.post("qanda/thread/byid/123", data='{"invalid_json":}')

    assert response.status_code == 500
    assert "An error occurred" in response.json["error"]


def test_get_question_general_error(test_client):
    with patch(
        "app.controller.qanda_controller.get_thread_by_id"
    ) as mock_get_thread_by_id:
        mock_get_thread_by_id.side_effect = Exception("Generic Error")

        response = test_client.post(
            "qanda/thread/byid/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 500
        assert "An error occurred" in response.json["error"]


def test_get_question_success(test_client):
    with patch(
        "app.controller.qanda_controller.get_thread_by_id"
    ) as mock_get_thread_by_id:
        mock_get_thread_by_id.return_value = {"question": "sample_question"}

        response = test_client.post(
            "qanda/thread/byid/123", json={"auth_token": "dummy_token"}
        )
        assert response.status_code == 200
        assert "question" in response.json

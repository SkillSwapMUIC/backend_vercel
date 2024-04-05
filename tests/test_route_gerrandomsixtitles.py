from json.decoder import JSONDecodeError
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.db import db
from app.models.question import Question
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


def test_get_random_six_titles_success(test_client):
    # Mocking the get_random_six_questions method to return dummy data
    with patch(
        "app.controller.qanda_controller.get_random_six_questions"
    ) as mock_get_random_six_questions:
        # Create Question instances
        question_1 = Question(title="Question 1", id=1)
        question_2 = Question(title="Question 2", id=2)
        question_3 = Question(title="Question 3", id=3)
        question_4 = Question(title="Question 4", id=4)
        question_5 = Question(title="Question 5", id=5)
        question_6 = Question(title="Question 6", id=6)

        # Mock the return value of get_random_six_questions to return a list of Question instances
        mock_get_random_six_questions.return_value = [
            question_1,
            question_2,
            question_3,
            question_4,
            question_5,
            question_6,
        ]
        response = test_client.get("qanda/getrandomsixtitles")
        assert response.status_code == 200
        assert len(response.json) == 6
        assert all("title" in item and "id" in item for item in response.json)


def test_get_random_six_titles_database_error(test_client):
    # Mocking the get_random_six_questions method to raise SQLAlchemyError
    with patch(
        "app.controller.qanda_controller.get_random_six_questions"
    ) as mock_get_random_six_questions:
        mock_get_random_six_questions.side_effect = SQLAlchemyError("Database Error")

        response = test_client.get("qanda/getrandomsixtitles")
        assert response.status_code == 500
        assert "Database error" in response.json["error"]


def test_get_random_six_titles_json_error(test_client):
    # Mocking the get_random_six_questions method to raise JSONDecodeError
    with patch(
        "app.controller.qanda_controller.get_random_six_questions"
    ) as mock_get_random_six_questions:
        mock_get_random_six_questions.side_effect = JSONDecodeError("JSON Error", "", 0)

        response = test_client.get("qanda/getrandomsixtitles")
        assert response.status_code == 500
        assert "JSON error" in response.json["error"]


def test_get_random_six_titles_general_error(test_client):
    # Mocking the get_random_six_questions method to raise a generic Exception
    with patch(
        "app.controller.qanda_controller.get_random_six_questions"
    ) as mock_get_random_six_questions:
        mock_get_random_six_questions.side_effect = Exception("Generic Error")

        response = test_client.get("/qanda/getrandomsixtitles")
        assert response.status_code == 500
        assert "An error occurred" in response.json["error"]

import json
from datetime import datetime

import pytest

from app.db import db
from app.models.question import Question
from index import app


@pytest.fixture
def client():

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_place_question(client):
    data = {
        "title": "Test Title",
        "question_text": "Test Question Text",
        "user_id": "test_user",
        "tags": ["test_tag1", "test_tag2"],
    }
    response = client.post("/submitQuestion", json=data)
    assert response.status_code == 200
    assert b"Placed a question" in response.data

    question = Question.query.filter_by(title="Test Title").first()
    assert question is not None
    assert question.title == "Test Title"
    assert question.question_text == "Test Question Text"
    assert question.user_id == "test_user"
    assert question.tags == "['test_tag1', 'test_tag2']"


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Get all" in response.data


def test_get_random_six_titles(client):

    response1 = client.get("/homepage/getrandomsixtitles")
    assert response1.status_code == 200

    data1 = json.loads(response1.data)
    assert len(data1) == 6

    response2 = client.get("/homepage/getrandomsixtitles")
    assert response2.status_code == 200

    data2 = json.loads(response2.data)
    assert len(data2) == 6

    assert data1 != data2


def test_get_question(client):
    with app.app_context():

        current_time = datetime.now()
        created_at = current_time.isoformat()

        test_question = Question(
            title="Test Title",
            question_text="Test Question Text",
            user_id="test_user",
            tags=str(["test_tag1", "test_tag2"]),
            created_at=created_at,
        )
        # Add the test question to the database
        db.session.add(test_question)
        db.session.commit()

        # Make a GET request to the endpoint
        response = client.get(f"/thread/byid/{test_question.id}")

        # Check if the response status code is 200 OK
        assert response.status_code == 200

        # Parse the JSON response
        response_data = json.loads(response.data)

        # Check if the returned data matches the expected data
        assert response_data["title"] == test_question.title
        assert response_data["question_text"] == test_question.question_text
        assert response_data["user_id"] == test_question.user_id
        assert response_data["tags"] == test_question.tags
        assert response_data["created_at"] == test_question.created_at

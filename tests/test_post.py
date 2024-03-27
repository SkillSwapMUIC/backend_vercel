import json
from datetime import datetime, timezone

import pytest

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


def add_sample_question():
    sample_question = Question(
        title="Sample Title",
        question_text="Sample Question Text",
        user_id="sample_user",
        tags="sample_tag1,sample_tag2",
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(sample_question)
    db.session.commit()
    return sample_question


def test_submit_question(test_client):
    data = {
        "title": "Test Title",
        "question_text": "Test Question Text",
        "user_id": "test_user",
        "tags": ["test_tag1", "test_tag2"],
    }
    response = test_client.post("/submitQuestion", json=data)
    assert response.status_code == 201
    assert "Question successfully placed" in response.get_json()["message"]


def test_submit_question_no_data(test_client):
    response = test_client.post("/submitQuestion", json={})
    assert response.status_code == 400
    assert "No input data provided" in response.get_json()["error"]


def test_get_random_six_titles(test_client):
    add_sample_question()

    response = test_client.get("/homepage/getrandomsixtitles")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) <= 6


def test_get_question(test_client):
    sample_question = add_sample_question()
    response = test_client.get(f"/thread/byid/{sample_question.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == sample_question.title


def test_get_question_not_found(test_client):
    response = test_client.get("/thread/byid/999")
    assert response.status_code == 404
    assert "Question not found" in response.get_json()["error"]


def test_question_repr():
    question = Question(
        id=1,
        title="Sample Question",
        question_text="What is the meaning of life?",
        user_id="user_123",
        tags="philosophy,life",
        created_at=datetime.now(),
    )
    assert repr(question) == "<Question 1>"


def test_delete_question(test_client):
    # Create a test question
    question = Question(
        id=1,
        title="Sample Question",
        question_text="What is the meaning of life?",
        user_id="user_123",
        tags="philosophy,life",
        created_at=datetime.now(),
    )
    db.session.add(question)
    db.session.commit()

    # Send a DELETE request to delete the question
    response = test_client.delete(f"/question/delete/{question.id}")

    # Check if the question is deleted successfully
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "message": f"Question with ID {question.id} deleted successfully"
    }


def test_update_question(test_client):
    # Create a test question
    question = Question(
        id=1,
        title="Sample Question",
        question_text="What is the meaning of life?",
        user_id="user_123",
        tags="philosophy,life",
        created_at=datetime.now(),
    )
    db.session.add(question)
    db.session.commit()

    # Data to update the question
    updated_data = {
        "title": "Updated Test Question",
        "question_text": "Updated test question text",
        "user_id": 123,
        "tags": str(["tag1", "tag2"]),
        "created_at": "2024-03-25T12:00:00",
    }

    # Send a PUT request to update the question
    response = test_client.put(f"/question/update/{question.id}", json=updated_data)

    # Check if the question is updated successfully
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "message": f"Question with ID {question.id} updated successfully"
    }

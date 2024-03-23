import pytest

from index import app, db
from models.question import Question


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_place_question(client):
    # Test placing a question
    data = {
        "title": "Test Title",
        "question_text": "Test Question Text",
        "user_id": "test_user",
        "tags": ["test_tag1", "test_tag2"],
    }
    response = client.post("/submitQuestion", json=data)
    assert response.status_code == 200
    assert b"Placed a question" in response.data

    # Check if question is stored in the database
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

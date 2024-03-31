import json
import pytest
from app import create_app
from app.db import db
from app.models.answer import Answer
from app.models.question import Question

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Füge Testdaten in die Datenbank ein
            data = {
                "title": "Test Question",
                "question_text": "This is a test question",
                "tags": ["test_tag1", "test_tag2"],
                "user_id": "test_user"
            }
            # Frage einfügen
            question_response = client.post("/qanda/question/submit", json=data)
            assert question_response.status_code == 201
            question_id = json.loads(question_response.data)["id"]

            # Antwort einfügen
            answer = Answer(content="Test Answer", question_id=question_id)
            db.session.add(answer)
            db.session.commit()

            # Antwort auf Antwort einfügen
            reply = Answer(content="Test Reply", parent_answer_id=answer.id)
            db.session.add(reply)
            db.session.commit()

            yield client  # Erweitern Sie den Bereich von client

            db.session.remove()
            db.drop_all()

def test_answer_question(client):
    response = client.post('/qanda/question/1/answer', json={"answer": "This is an answer"})
    print(response.data)
    assert response.status_code == 201
    assert b"Answer submitted successfully" in response.data

def test_get_answers(client):
    response = client.get('/qanda/question/1/answers')
    print(response.data)
    assert response.status_code == 200
    assert b"Test Answer" in response.data

def test_reply_to_answer(client):
    response = client.post('/qanda/answer/1/reply', json={"reply": "This is a reply"})
    print(response.data)
    assert response.status_code == 201
    assert b"Reply submitted successfully" in response.data

def test_get_replies(client):
    response = client.get('/qanda/answers/1/replies')
    print(response.data)
    assert response.status_code == 200
    assert b"Test Reply" in response.data

def test_get_answers_and_replies(client):
    response = client.get('qanda/questions/1/answers/replies')
    print(response.data)
    assert response.status_code == 200
    assert b"Test Answer" in response.data
    assert b"Test Reply" in response.data

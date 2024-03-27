import json
import pytest
from flask import Flask
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_autocomplete_with_results(client):
    data = {
        "title": "Test Title",
        "question_text": "Test Question Text",
        "user_id": "test_user",
        "tags": ["test_tag1", "test_tag2"],
    }
    response = client.post("/qanda/question/submit", json=data)
    assert response.status_code == 201
    assert "Question successfully placed" in response.get_json()["message"]

    response2 = client.get('/search/searchbar/autocomplete?search=Test')
    print(response2.data)
    data = json.loads(response2.data.decode('utf-8'))

    assert response2.status_code == 200
    assert len(data) > 0

def test_autocomplete_with_no_results(client):
    response = client.get('/search/searchbar/autocomplete?search=nonexistent')
    print(response.data)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 404
    assert "message" in data
    assert data["message"] == "Nothing was found"

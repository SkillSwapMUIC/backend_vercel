from datetime import datetime, timezone

import pytest

from app.db import db
from app.models.course import Course
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


def add_course(title, description, category, level, votes_up, creator_id=1):
    course = Course(
        title=title,
        description=description,
        category=category,
        level=level,
        votes_up=votes_up,
        created_at=datetime.now(timezone.utc),
        creator_id=creator_id,
    )
    db.session.add(course)
    db.session.commit()
    return course


def test_create_course(test_client):
    data = {
        "title": "New Course",
        "description": "A new course description",
        "category": "Mathematics",
        "level": "Beginner",
        "votes_up": 0,
        "creator_id": 1,
    }
    response = test_client.post("/course/manage", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Course added successfully"


def test_get_course(test_client):
    course = add_course("Test Course", "Description", "Science", "Intermediate", 10)
    response = test_client.get(f"/course/{course.id}")
    assert response.status_code == 200
    assert response.json["title"] == "Test Course"
    assert response.json["description"] == "Description"
    assert response.json["category"] == "Science"
    assert response.json["level"] == "Intermediate"


def test_update_course(test_client):
    course = add_course("Old Course", "Old description", "History", "Advanced", 5)
    data = {
        "title": "Updated Course",
        "description": "Updated description",
    }
    response = test_client.put(f"/course/{course.id}", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Course updated successfully"


def test_delete_course(test_client):
    course = add_course("To Be Deleted", "Description", "Art", "All levels", 0)
    response = test_client.delete(f"/course/{course.id}")
    assert response.status_code == 200
    assert response.json["message"] == "Course deleted successfully"


def test_course_repr(test_client):
    course = Course(title="Test Course", creator_id=1)
    assert repr(course) == "<Course Test Course>"

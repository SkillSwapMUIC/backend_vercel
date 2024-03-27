import uuid

import pytest

from app.db import db
from app.models.user import User
from index import app


@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        test_user = User(
            email="test@example.com",
            name="Test User",
            profile_picture="http://example.com/pic.jpg",
            google_id="test_google_id",
        )
        db.session.add(test_user)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_google_login(test_client):
    response = test_client.post("/user/auth/google")
    assert response.status_code == 501  # Not Implemented
    assert response.json["message"] == "Google SSO integration to be implemented"


def test_logout(test_client):
    response = test_client.post("/user/auth/logout")
    assert response.status_code == 501  # Not Implemented
    assert response.json["message"] == "Logout functionality to be implemented"


def test_update_user_profile_with_valid_data(test_client):
    update_data = {
        "name": "Updated Test User",
        "profile_picture": "http://example.com/newpic.jpg",
    }
    response = test_client.put("/user/me", json=update_data)
    assert response.status_code == 200
    assert response.json["message"] == "Profile updated successfully"

    response = test_client.get("/user/me")
    data = response.json
    assert data["name"] == update_data["name"]
    assert data["profile_picture"] == update_data["profile_picture"]


def test_update_user_profile_with_invalid_data(test_client):
    update_data = {"name": ""}
    response = test_client.put("/user/me", json=update_data)
    assert response.status_code == 400
    assert "error" in response.json


def test_get_user_profile(test_client):
    response = test_client.get("/user/me")
    assert response.status_code == 200
    data = response.json
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["profile_picture"] == "http://example.com/pic.jpg"


def test_user_repr(test_client):
    with app.app_context():
        unique_email = f"test{uuid.uuid4()}@example.com"
        user = User(email=unique_email, name="Test User")
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(email=unique_email).first()
        assert saved_user is not None
        assert repr(saved_user) == f"<User {saved_user.email}>"


def test_user_model_properties():
    user = User(
        email="unique@example.com",
        name="Unique Name",
        profile_picture="http://example.com/unique.jpg",
        google_id="unique_google_id",
    )
    assert user.email == "unique@example.com"
    assert user.name == "Unique Name"
    assert user.profile_picture == "http://example.com/unique.jpg"
    assert user.google_id == "unique_google_id"

import pytest

from index import app
from models.user import User
from project_objects import db


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
    response = test_client.post("/api/auth/google")
    assert response.status_code == 501  # Not Implemented
    assert response.json["message"] == "Google SSO integration to be implemented"


def test_logout(test_client):
    response = test_client.post("/api/auth/logout")
    assert response.status_code == 501  # Not Implemented
    assert response.json["message"] == "Logout functionality to be implemented"


def test_update_user_profile(test_client):
    update_data = {
        "name": "Updated Test User",
        "profile_picture": "http://example.com/newpic.jpg",
    }
    response = test_client.put("/api/users/me", json=update_data)
    assert response.status_code == 200
    assert response.json["message"] == "Profile updated successfully"

    # Fetch again to verify update
    response = test_client.get("/api/users/me")
    data = response.json
    assert data["name"] == update_data["name"]
    assert data["profile_picture"] == update_data["profile_picture"]


def test_get_user_profile(test_client):
    response = test_client.get("/api/users/me")
    assert response.status_code == 200
    data = response.json
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["profile_picture"] == "http://example.com/pic.jpg"

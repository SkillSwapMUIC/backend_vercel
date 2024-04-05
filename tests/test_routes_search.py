from unittest.mock import patch

import pytest

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


def test_autocomplete_success(test_client):
    with patch(
        "app.routes.search.search_for_post_by_key"
    ) as mock_search_for_post_by_key:
        mock_search_for_post_by_key.return_value = [
            {"title": "Post 1", "id": 1},
            {"title": "Post 2", "id": 2},
        ]

        response = test_client.post(
            "search/searchbar/autocomplete", json={"search_key": "query"}
        )
        assert response.status_code == 200
        assert len(response.json) == 2
        assert all("title" in item and "id" in item for item in response.json)


def test_autocomplete_no_results(test_client):
    with patch(
        "app.routes.search.search_for_post_by_key"
    ) as mock_search_for_post_by_key:
        mock_search_for_post_by_key.return_value = []

        response = test_client.post(
            "search/searchbar/autocomplete", json={"search_key": "query"}
        )
        assert response.status_code == 200
        assert response.json == []

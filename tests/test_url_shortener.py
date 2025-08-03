import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    data = response.get_json()
    assert response.status_code == 200
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "invalid-url"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid URL"

def test_redirect_existing_code(client):
    post_response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    short_code = post_response.get_json()["short_code"]

    get_response = client.get(f"/{short_code}", follow_redirects=False)
    assert get_response.status_code == 302
    assert get_response.headers["Location"] == "https://www.example.com"

def test_redirect_invalid_code(client):
    response = client.get("/xyz123")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Short code not found"

def test_analytics_endpoint(client):
    post_response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    short_code = post_response.get_json()["short_code"]

    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    stats_response = client.get(f"/api/stats/{short_code}")
    data = stats_response.get_json()

    assert stats_response.status_code == 200
    assert data["url"] == "https://www.example.com"
    assert data["clicks"] == 2
    assert "created_at" in data

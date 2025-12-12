from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_about():
    response = client.get("/about")
    assert response.status_code == 200
    assert "About Me" in response.text  # Adjust based on actual content

def test_read_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert "Projects" in response.text  # Adjust based on actual content

def test_read_skills():
    response = client.get("/skills")
    assert response.status_code == 200
    assert "Skills" in response.text  # Adjust based on actual content

def test_read_contact():
    response = client.get("/contact")
    assert response.status_code == 200
    assert "Contact" in response.text  # Adjust based on actual content

def test_contact_form_submission():
    response = client.post("/contact", json={
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message."
    })
    assert response.status_code == 200
    assert response.json() == {"detail": "Message sent successfully."}  # Adjust based on actual response
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.services.json_utils import read_json, write_json
from app.services.data_manager import DataManager

app = FastAPI()
client = TestClient(app)

# Sample data for testing
sample_projects = {
    "projects": [
        {
            "id": "project-1",
            "title": "Test Project",
            "description": "A project for testing purposes.",
            "technologies": ["Python", "FastAPI"],
            "image": "test_project.jpg",
            "github_url": "https://github.com/test/project",
            "live_url": "https://testproject.com",
            "featured": False,
            "created_date": "2023-01-01"
        }
    ]
}

sample_skills = {
    "skills": [
        {
            "id": "skill-1",
            "name": "Test Skill",
            "category": "Testing",
            "proficiency": 80,
            "years_experience": 2,
            "icon": "test_skill.svg"
        }
    ]
}

# Test for JSON utility functions
def test_read_json():
    write_json("data/projects.json", sample_projects)
    data = read_json("data/projects.json")
    assert data == sample_projects

def test_write_json():
    new_data = {
        "projects": [
            {
                "id": "project-2",
                "title": "Another Test Project",
                "description": "Another project for testing.",
                "technologies": ["JavaScript", "React"],
                "image": "another_project.jpg",
                "github_url": "https://github.com/test/another_project",
                "live_url": "https://anotherproject.com",
                "featured": True,
                "created_date": "2023-02-01"
            }
        ]
    }
    write_json("data/projects.json", new_data)
    data = read_json("data/projects.json")
    assert data == new_data

# Test for DataManager class
def test_data_manager():
    data_manager = DataManager("data/projects.json")
    data_manager.write_data(sample_projects)
    data = data_manager.read_data()
    assert data == sample_projects

    # Clean up
    data_manager.write_data({"projects": []})  # Reset data after test
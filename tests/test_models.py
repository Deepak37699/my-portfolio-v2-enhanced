from fastapi import HTTPException
from app.models.project import Project
from app.models.skill import Skill
from app.models.user import User
from app.models.contact import Contact

def test_project_model():
    project_data = {
        "id": "project-1",
        "title": "Portfolio Website",
        "description": "Personal portfolio using FastAPI",
        "technologies": ["Python", "FastAPI", "HTML/CSS"],
        "image": "portfolio.jpg",
        "github_url": "https://github.com/username/portfolio",
        "live_url": "https://myportfolio.com",
        "featured": True,
        "created_date": "2023-05-15"
    }
    project = Project(**project_data)
    assert project.id == "project-1"
    assert project.title == "Portfolio Website"
    assert project.description == "Personal portfolio using FastAPI"
    assert project.technologies == ["Python", "FastAPI", "HTML/CSS"]
    assert project.image == "portfolio.jpg"
    assert project.github_url == "https://github.com/username/portfolio"
    assert project.live_url == "https://myportfolio.com"
    assert project.featured is True
    assert project.created_date == "2023-05-15"

def test_skill_model():
    skill_data = {
        "id": "skill-1",
        "name": "Python",
        "category": "Programming Language",
        "proficiency": 90,
        "years_experience": 3,
        "icon": "python-icon.svg"
    }
    skill = Skill(**skill_data)
    assert skill.id == "skill-1"
    assert skill.name == "Python"
    assert skill.category == "Programming Language"
    assert skill.proficiency == 90
    assert skill.years_experience == 3
    assert skill.icon == "python-icon.svg"

def test_user_model():
    user_data = {
        "username": "admin",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
        "created_date": "2023-05-10"
    }
    user = User(**user_data)
    assert user.username == "admin"
    assert user.hashed_password == "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    assert user.is_active is True
    assert user.created_date == "2023-05-10"

def test_contact_model():
    contact_data = {
        "id": "message-1",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "message": "Hello, this is a test message.",
        "created_date": "2023-05-20"
    }
    contact = Contact(**contact_data)
    assert contact.id == "message-1"
    assert contact.name == "John Doe"
    assert contact.email == "john.doe@example.com"
    assert contact.message == "Hello, this is a test message."
    assert contact.created_date == "2023-05-20"
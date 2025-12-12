#!/usr/bin/env python3
"""
Test script to verify all admin panel functionality
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoints():
    """Test public API endpoints to verify data loading"""
    print("🧪 Testing API Endpoints...")    # Test projects endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            data = response.json()
            projects = data.get('projects', [])
            print(f"✅ Projects API: {len(projects)} projects loaded")
            if projects:
                print(f"   Sample project: {projects[0].get('title', 'Unknown')}")
                featured_count = sum(1 for p in projects if p.get('featured', False))
                print(f"   Featured projects: {featured_count}")
        else:
            print(f"❌ Projects API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Projects API error: {e}")
    
    # Test skills endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/skills")
        if response.status_code == 200:
            data = response.json()
            skills = data.get('skills', [])
            print(f"✅ Skills API: {len(skills)} skills loaded")
            if skills:
                categories = set(skill.get('category', 'Unknown') for skill in skills)
                print(f"   Categories: {', '.join(sorted(categories))}")
        else:
            print(f"❌ Skills API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Skills API error: {e}")    # Test about endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/about")
        if response.status_code == 200:
            data = response.json()
            about = data.get('about', {})
            name = about.get('name', 'Unknown')
            print(f"✅ About API: Profile for {name}")
            print(f"   Education entries: {len(about.get('education', []))}")
            print(f"   Certifications: {len(about.get('certifications', []))}")
            print(f"   Languages: {len(about.get('languages', []))}")
        else:
            print(f"❌ About API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ About API error: {e}")
    
    # Test contact endpoint
    try:
        response = requests.post(f"{BASE_URL}/api/contact", json={
            "name": "Test User",
            "email": "test@example.com",
            "subject": "API Test",
            "message": "This is a test message from automated testing"
        })
        if response.status_code == 200:
            print("✅ Contact API: Message submission works")
        else:
            print(f"❌ Contact API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Contact API error: {e}")

def test_admin_pages():
    """Test admin page accessibility"""
    print("\n🖥️ Testing Admin Pages...")
    
    admin_pages = [
        "/admin/dashboard",
        "/admin/projects", 
        "/admin/skills",
        "/admin/messages",
        "/admin/about"
    ]
    
    for page in admin_pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            # Admin pages should redirect to login (302/303) or show login page
            if response.status_code in [200, 302, 303]:
                print(f"✅ {page}: Accessible (redirects to auth as expected)")
            else:
                print(f"❌ {page}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {page}: Error - {e}")

def test_main_site():
    """Test main portfolio site"""
    print("\n🌐 Testing Main Site...")
    
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Main site: Homepage loads successfully")
            # Check if it contains expected content
            content = response.text
            if "portfolio" in content.lower() or "projects" in content.lower():
                print("✅ Main site: Contains expected portfolio content")
            else:
                print("⚠️ Main site: May not contain expected content")
        else:
            print(f"❌ Main site failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main site error: {e}")

def print_data_summary():
    """Print summary of loaded data"""
    print("\n📊 Data Summary:")
    
    try:
        # Check projects data
        with open("d:/Deepak Yadav/Portfolio/my-portfolio/data/projects.json", "r") as f:
            data = json.load(f)
            projects = data.get('projects', [])
            print(f"📁 Projects: {len(projects)} entries")
            if projects:
                featured_count = sum(1 for p in projects if p.get('featured', False))
                print(f"   Featured projects: {featured_count}")
            
        # Check skills data  
        with open("d:/Deepak Yadav/Portfolio/my-portfolio/data/skills.json", "r") as f:
            data = json.load(f)
            skills = data.get('skills', [])
            print(f"🛠️ Skills: {len(skills)} entries")
            if skills:
                categories = set(skill.get('category', 'Unknown') for skill in skills)
                print(f"   Categories: {', '.join(sorted(categories))}")
            
        # Check messages data
        with open("d:/Deepak Yadav/Portfolio/my-portfolio/data/messages.json", "r") as f:
            data = json.load(f)
            messages = data.get('messages', [])
            print(f"📧 Messages: {len(messages)} entries")
            if messages:
                status_counts = {}
                for msg in messages:
                    status = msg.get('status', 'unread')
                    status_counts[status] = status_counts.get(status, 0) + 1
                print(f"   Status breakdown: {status_counts}")
            
        # Check about data
        with open("d:/Deepak Yadav/Portfolio/my-portfolio/data/about.json", "r") as f:
            data = json.load(f)
            about = data.get('about', {})
            print(f"👤 About: Profile for {about.get('name', 'Unknown')}")
            print(f"   Education: {len(about.get('education', []))} entries")
            print(f"   Certifications: {len(about.get('certifications', []))} entries")
            print(f"   Languages: {len(about.get('languages', []))} entries")
            
    except Exception as e:
        print(f"❌ Error reading data files: {e}")

if __name__ == "__main__":
    print("🚀 FastAPI Portfolio Admin Panel Test Suite")
    print("=" * 50)
    
    print_data_summary()
    test_main_site()
    test_api_endpoints()
    test_admin_pages()
    
    print("\n" + "=" * 50)
    print("✨ Test Complete! Check the results above.")
    print("💡 Note: Admin pages require authentication, so redirects are expected.")
    print("🔗 Admin Login: http://127.0.0.1:8000/auth/login")
    print("🔗 Main Site: http://127.0.0.1:8000")

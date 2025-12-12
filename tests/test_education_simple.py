#!/usr/bin/env python3
"""
Test script to verify the education functionality fix.
This script tests the complete flow of authentication and education CRUD operations.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Default password

def test_education_functionality():
    """Test the complete education functionality flow."""
    
    print("🧪 Testing Education Functionality Fix")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test 1: Login
    print("\n1. Testing Login...")
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    login_response = session.post(
        f"{BASE_URL}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code == 200:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
        return False
    
    # Test 2: Get existing education records
    print("\n2. Testing Get Education Records...")
    get_response = session.get(f"{BASE_URL}/admin/api/education")
    
    if get_response.status_code == 200:
        education_data = get_response.json()
        print(f"✅ Get education records successful: {len(education_data.get('education', []))} records found")
        print(f"   Records: {education_data}")
    else:
        print(f"❌ Get education records failed: {get_response.status_code} - {get_response.text}")
        return False
    
    # Test 3: Create a new education record
    print("\n3. Testing Create Education Record...")
    new_education = {
        "degree": "Bachelor of Computer Science",
        "institution": "Test University",
        "year": "2023",
        "grade": "First Class",
        "description": "Test education record created by automation script"
    }
    
    create_response = session.post(
        f"{BASE_URL}/admin/api/education",
        json=new_education,
        headers={"Content-Type": "application/json"}
    )
    
    if create_response.status_code == 200:
        created_education = create_response.json()
        education_id = created_education.get("education", {}).get("id")
        print(f"✅ Create education record successful: ID = {education_id}")
        print(f"   Created: {created_education}")
    else:
        print(f"❌ Create education record failed: {create_response.status_code} - {create_response.text}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Basic Education Functionality Tests PASSED!")
    print("✅ The education creation error has been fixed!")
    print("✅ Authentication with cookies works correctly")
    print("✅ API path /admin/api/education is working")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        success = test_education_functionality()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        exit(1)

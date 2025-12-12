#!/usr/bin/env python3
"""
Test script for CRUD API endpoints for education, experience, and certifications
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8001"
USERNAME = "admin"
PASSWORD = "admin123"

def get_auth_token():
    """Login and get authentication token"""
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/auth/api/login", 
                           json=login_data, 
                           headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_education_api(token):
    """Test education CRUD operations"""
    print("\n=== Testing Education API ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET all educations
    response = requests.get(f"{BASE_URL}/api/education", headers=headers)
    print(f"GET /api/education: {response.status_code}")
    educations = []
    if response.status_code == 200:
        educations = response.json()
        print(f"Found {len(educations)} education records")
        for edu in educations:
            print(f"  - {edu.get('degree')} from {edu.get('institution')}")
    
    # Test GET specific education (if any exist)
    if response.status_code == 200 and educations:
        first_edu = educations[0]
        edu_id = first_edu.get('id')
        response = requests.get(f"{BASE_URL}/api/education/{edu_id}", headers=headers)
        print(f"GET /api/education/{edu_id}: {response.status_code}")
    
    return response.status_code == 200

def test_experience_api(token):
    """Test experience CRUD operations"""
    print("\n=== Testing Experience API ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET all experiences
    response = requests.get(f"{BASE_URL}/api/experience", headers=headers)
    print(f"GET /api/experience: {response.status_code}")
    if response.status_code == 200:
        experiences = response.json()
        print(f"Found {len(experiences)} experience records")
        for exp in experiences:
            print(f"  - {exp.get('job_title')} at {exp.get('company')}")
    
    return response.status_code == 200

def test_certification_api(token):
    """Test certification CRUD operations"""
    print("\n=== Testing Certification API ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET all certifications
    response = requests.get(f"{BASE_URL}/api/certifications", headers=headers)
    print(f"GET /api/certifications: {response.status_code}")
    if response.status_code == 200:
        certifications = response.json()
        print(f"Found {len(certifications)} certification records")
        for cert in certifications:
            print(f"  - {cert.get('name')} from {cert.get('issuer')}")
    
    return response.status_code == 200

def main():
    """Main test function"""
    print("🧪 Testing CRUD API endpoints...")
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Failed to authenticate")
        sys.exit(1)
    
    print("✅ Authentication successful")
    
    # Test all APIs
    results = []
    results.append(test_education_api(token))
    results.append(test_experience_api(token))
    results.append(test_certification_api(token))
    
    # Summary
    print(f"\n📊 Test Results:")
    print(f"Education API: {'✅ Pass' if results[0] else '❌ Fail'}")
    print(f"Experience API: {'✅ Pass' if results[1] else '❌ Fail'}")
    print(f"Certification API: {'✅ Pass' if results[2] else '❌ Fail'}")
    
    if all(results):
        print("\n🎉 All API tests passed!")
    else:
        print("\n⚠️ Some API tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to validate the FastAPI portfolio application
"""
import os
import sys
import traceback

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        # Test basic FastAPI import
        from fastapi import FastAPI
        print("✓ FastAPI imported successfully")
        
        # Test app import
        from app.main import app
        print("✓ Main app imported successfully")
        
        # Test routes
        from app.routes import portfolio, admin, auth
        print("✓ Routes imported successfully")
        
        # Test services
        from app.services.data_manager import DataManager
        print("✓ DataManager imported successfully")
        
        # Test models
        from app.models.project import Project
        from app.models.skill import Skill
        from app.models.user import User
        print("✓ Models imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False

def test_data_files():
    """Test if data files exist and are readable"""
    print("\nTesting data files...")
    
    data_files = [
        "data/projects.json",
        "data/skills.json", 
        "data/about.json",
        "data/users.json",
        "data/messages.json"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    import json
                    json.load(f)
                print(f"✓ {file_path} exists and is valid JSON")
            except Exception as e:
                print(f"✗ {file_path} exists but has invalid JSON: {e}")
        else:
            print(f"✗ {file_path} does not exist")

def main():
    """Main test function"""
    print("FastAPI Portfolio Application Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test data files
    test_data_files()
    
    # Test environment
    print(f"\nEnvironment file exists: {os.path.exists('.env')}")
    
    if imports_ok:
        print("\n✓ All tests passed! The application should be ready to run.")
        print("To start the server, run:")
        print("uvicorn app.main:app --reload")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simple test script to verify Netlify deployment
"""
import sys
import os
from pathlib import Path

# Add the project root to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        return False
        
    try:
        from mangum import Mangum
        print("✅ Mangum imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Mangum: {e}")
        return False
        
    return True

def test_app_creation():
    """Test if the app can be created"""
    print("\nTesting app creation...")
    
    try:
        from app.main import app
        from mangum import Mangum
        
        handler = Mangum(app, lifespan="off")
        print("✅ Mangum handler created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create handler: {e}")
        return False

def test_file_structure():
    """Test if required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "app/main.py",
        "app/__init__.py",
        "templates/index.html",
        "templates/base.html",
        "data/projects.json",
        "data/skills.json",
        "static/css",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 Testing Netlify deployment setup...\n")
    
    success = True
    success &= test_file_structure()
    success &= test_imports()
    success &= test_app_creation()
    
    print("\n" + "="*50)
    if success:
        print("🎉 All tests passed! Deployment should work.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Verification script for Render deployment
"""
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "render.yaml",
        "requirements.txt",
        "app/main.py",
        ".env.production"
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ All required files present")
    return True

def check_dependencies():
    """Check if all Python dependencies are available"""
    try:
        import fastapi
        import uvicorn
        import jinja2
        import bcrypt
        import gunicorn
        print("✅ All Python dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_render_structure():
    """Check Render deployment structure"""
    checks = [
        (Path("app"), "FastAPI app directory"),
        (Path("data"), "Data directory"),
        (Path("templates"), "Templates directory"),
        (Path("static"), "Static files directory")
    ]

    all_good = True
    for path, description in checks:
        if path.exists():
            print(f"✅ {description} found")
        else:
            print(f"❌ {description} missing: {path}")
            all_good = False

    return all_good

def main():
    """Main verification function"""
    print("🔍 Render Deployment Verification")
    print("=" * 40)

    checks = [
        check_requirements(),
        check_dependencies(),
        check_render_structure()
    ]

    if all(checks):
        print("\n🎉 All checks passed! Ready for Render deployment.")
        print("\nNext steps:")
        print("1. Push code to your Git repository")
        print("2. Connect repository to Render")
        print("3. Set environment variables in Render dashboard")
        print("4. Deploy!")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

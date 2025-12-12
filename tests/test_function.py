#!/usr/bin/env python3
"""
Test the Netlify function locally to simulate the serverless environment
"""
import sys
import os
from pathlib import Path

# Change to the functions directory to simulate Netlify environment
functions_dir = Path(__file__).parent / "netlify" / "functions"
os.chdir(functions_dir)

# Add current directory to Python path
sys.path.insert(0, '.')

def test_function():
    """Test the main function"""
    print("Testing Netlify function...")
    
    # Import the function
    from main import main
    
    # Create a test event (simulate a GET request to the home page)
    test_event = {
        'httpMethod': 'GET',
        'path': '/',
        'headers': {},
        'queryStringParameters': None,
        'body': None,
        'isBase64Encoded': False
    }
    
    test_context = {}
    
    # Call the function
    response = main(test_event, test_context)
    
    print(f"Response status: {response.get('statusCode', 'Unknown')}")
    print(f"Response headers: {response.get('headers', {})}")
    
    # Check if it's successful
    if response.get('statusCode') == 200:
        print("✅ Function returned 200 OK")
        return True
    else:
        print(f"❌ Function returned {response.get('statusCode')}")
        print(f"Body: {response.get('body', '')[:200]}...")
        return False

if __name__ == "__main__":
    try:
        success = test_function()
        if success:
            print("\n🎉 Netlify function test passed!")
        else:
            print("\n⚠️ Netlify function test failed!")
    except Exception as e:
        print(f"\n❌ Error testing function: {e}")
        import traceback
        traceback.print_exc()

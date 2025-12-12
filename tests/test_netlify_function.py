#!/usr/bin/env python3
"""
Test script to verify the Netlify function works correctly
"""
import sys
import os
from pathlib import Path

def test_function():
    """Test the Netlify function locally"""
    try:
        # Add netlify functions directory to path
        functions_dir = Path(__file__).parent / "netlify" / "functions"
        sys.path.insert(0, str(functions_dir))
        
        # Change to functions directory
        original_cwd = os.getcwd()
        os.chdir(str(functions_dir))
        
        # Import the handler (suppress IDE warning - this works at runtime)
        import main  # type: ignore
        handler = main.handler
        
        # Restore original directory
        os.chdir(original_cwd)
        
        # Create a mock event and context (similar to what Netlify sends)
        mock_event = {
            "httpMethod": "GET",
            "path": "/",
            "headers": {
                "host": "localhost:8000",
                "user-agent": "test-agent"
            },
            "multiValueHeaders": {
                "accept": ["text/html"]
            },
            "queryStringParameters": None,
            "multiValueQueryStringParameters": None,
            "body": None,
            "isBase64Encoded": False,
            "resource": "/",
            "stageVariables": None,
            "requestContext": {
                "accountId": "123456789012",
                "resourceId": "123456",
                "stage": "test",
                "requestId": "test-request-id",
                "identity": {
                    "sourceIp": "127.0.0.1",
                    "userAgent": "test-agent"
                },
                "resourcePath": "/",
                "httpMethod": "GET"
            }
        }
        
        mock_context = {
            "requestId": "test-request-id",
            "stage": "test"
        }
        
        # Call the handler
        response = handler(mock_event, mock_context)
        
        print("✅ Function test successful!")
        print(f"Status Code: {response.get('statusCode', 'Unknown')}")
        print(f"Headers: {response.get('headers', {})}")
        
        # Check if it's an HTML response
        body = response.get('body', '')
        if 'html' in body.lower():
            print("📄 Response contains HTML content")
        
        return True
        
    except Exception as e:
        print(f"❌ Function test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Netlify function...")
    success = test_function()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test script with proper Netlify Functions event format
"""
import sys
import os
from pathlib import Path

def test_function():
    """Test the Netlify function with proper event format"""
    try:
        # Add netlify functions directory to path
        functions_dir = Path(__file__).parent / "netlify" / "functions"
        sys.path.insert(0, str(functions_dir))
        
        # Change to functions directory
        original_cwd = os.getcwd()
        os.chdir(str(functions_dir))
        
        # Import the handler
        import main
        handler = main.handler
        
        # Restore original directory
        os.chdir(original_cwd)
        
        # Create a proper Netlify Functions event
        netlify_event = {
            "httpMethod": "GET",
            "path": "/",
            "multiValueHeaders": {},
            "multiValueQueryStringParameters": None,
            "headers": {
                "Host": "localhost:8888",
                "User-Agent": "test-agent/1.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            },
            "queryStringParameters": None,
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "1234567890",
                "protocol": "HTTP/1.1",
                "httpMethod": "GET",
                "path": "/",
                "stage": "prod",
                "requestId": "test-request-id",
                "requestTime": "01/Jan/2025:00:00:00 +0000",
                "requestTimeEpoch": 1640995200,
                "identity": {
                    "sourceIp": "127.0.0.1",
                    "userAgent": "test-agent/1.0"
                }
            }
        }
        
        netlify_context = {
            "callbackWaitsForEmptyEventLoop": True,
            "functionName": "main",
            "functionVersion": "$LATEST",
            "invokedFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:main",
            "memoryLimitInMB": "1024",
            "awsRequestId": "test-request-id",
            "logGroupName": "/aws/lambda/main",
            "logStreamName": "2025/01/01/[$LATEST]test",
            "getRemainingTimeInMillis": lambda: 30000
        }
        
        # Call the handler
        response = handler(netlify_event, netlify_context)
        
        print("✅ Function test successful!")
        print(f"Status Code: {response.get('statusCode', 'Unknown')}")
        print(f"Headers: {response.get('headers', {})}")
        
        # Check if it's an HTML response
        body = response.get('body', '')
        if 'html' in body.lower():
            print("📄 Response contains HTML content")
            # Print first 200 chars of body for debugging
            print(f"Body preview: {body[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Function test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Netlify function with proper event format...")
    success = test_function()
    sys.exit(0 if success else 1)

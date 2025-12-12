#!/usr/bin/env python3
"""
Monitor Netlify deployment and test the functions
"""
import requests
import time
import sys

def test_url(url, expected_status=200, description=""):
    """Test a URL and report results"""
    try:
        print(f"🧪 Testing {description}: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ SUCCESS: Status {response.status_code}")
            if "html" in response.headers.get('content-type', '').lower():
                content_preview = response.text[:200].replace('\n', ' ')
                print(f"📄 Content preview: {content_preview}...")
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"📄 Response: {response.text[:300]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("🚀 Netlify Deployment Monitor")
    print("=" * 50)
    
    # Get base URL from user or use default pattern
    base_url = input("Enter the new deployment URL (or press Enter to wait): ").strip()
    
    if not base_url:
        print("⏱️  Waiting for deployment to complete...")
        print("💡 Check Netlify dashboard for new deployment URL")
        print("💡 URL pattern: https://[DEPLOY-ID]--deepak37699.netlify.app/")
        return
    
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}"
    
    if not base_url.endswith('/'):
        base_url += '/'
    
    print(f"🎯 Testing deployment: {base_url}")
    print()
    
    # Test sequence
    tests = [
        (f"{base_url}test", "Simple Test Function"),
        (f"{base_url}.netlify/functions/main", "FastAPI Main Function"), 
        (f"{base_url}", "Root URL (with redirect)")
    ]
    
    results = []
    for url, description in tests:
        success = test_url(url, description=description)
        results.append((description, success))
        print()
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("📊 TEST SUMMARY")
    print("=" * 30)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {description}")
    
    print(f"\n🏆 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Deployment successful!")
    elif passed > 0:
        print("⚠️  Partial success - some functions working")
    else:
        print("💥 All tests failed - check deployment logs")

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Script to test API endpoints after deployment
"""
import requests
import json

def test_api_endpoints(base_url):
    """Test all API endpoints"""
    print(f"🧪 Testing API endpoints at: {base_url}")
    
    endpoints = [
        '/api/health/',
        '/api/interview-scripts/',
        '/admin/',
    ]
    
    results = []
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
            results.append({
                'endpoint': endpoint,
                'status_code': response.status_code,
                'status': status
            })
            print(f"{status} {endpoint} - Status: {response.status_code}")
        except Exception as e:
            results.append({
                'endpoint': endpoint,
                'status_code': 'ERROR',
                'status': '❌ FAIL',
                'error': str(e)
            })
            print(f"❌ FAIL {endpoint} - Error: {e}")
    
    return results

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python test_api.py <your-vercel-url>")
        print("Example: python test_api.py https://mortguage.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    results = test_api_endpoints(base_url)
    
    # Summary
    passed = sum(1 for r in results if r['status'] == '✅ PASS')
    total = len(results)
    
    print(f"\n📊 Test Summary: {passed}/{total} endpoints passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is ready!")
    else:
        print("⚠️  Some tests failed. Check the logs above.")

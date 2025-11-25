from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

def test_ui_endpoints():
    print("\n--- Testing UI Endpoints ---")
    
    # 1. Root (Index)
    response = client.get("/")
    print(f"GET /: {response.status_code}")
    assert response.status_code == 200
    assert "TradingWizard" in response.text

    # 2. Static CSS
    response = client.get("/static/style.css")
    print(f"GET /static/style.css: {response.status_code}")
    assert response.status_code == 200

    # 3. Static JS
    response = client.get("/static/script.js")
    print(f"GET /static/script.js: {response.status_code}")
    assert response.status_code == 200

    # 4. Trends API
    response = client.get("/trends")
    print(f"GET /trends: {response.status_code}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(f"Trends: {response.json()}")

if __name__ == "__main__":
    try:
        test_ui_endpoints()
        print("\nUI VERIFICATION PASSED")
    except AssertionError as e:
        print(f"\nUI VERIFICATION FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        exit(1)

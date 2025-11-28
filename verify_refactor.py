import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_config_registration_disabled():
    print("\n--- Testing Registration Disabled ---")
    # 1. Disable registration in config
    with open("app_config.json", "r") as f:
        config = json.load(f)
    
    original_setting = config.get("registration_enabled", True)
    config["registration_enabled"] = False
    
    with open("app_config.json", "w") as f:
        json.dump(config, f)

    # Restart app or wait for reload? 
    # Since we can't restart the app easily from here, we rely on the fact that ConfigService loads on init.
    # However, ConfigService is a Singleton and might already be loaded. 
    # In a real scenario, we'd restart. Here, we might need to restart the server manually or mock.
    # For this script, let's assume we can't easily restart and just skip this check if it requires restart,
    # BUT, our ConfigService loads from file on __new__. If we create a new instance (or if the app reloads), it should work.
    # Let's try to hit the endpoint.
    
    try:
        response = requests.post(f"{BASE_URL}/users", json={
            "username": "testuser_disabled",
            "email": "disabled@example.com",
            "password": "password123"
        })
        if response.status_code == 403:
            print("SUCCESS: Registration correctly blocked.")
        else:
            print(f"FAILURE: Expected 403, got {response.status_code}. (Note: App might need restart to pick up config change)")
    finally:
        # Restore config
        config["registration_enabled"] = original_setting
        with open("app_config.json", "w") as f:
            json.dump(config, f)

def test_pagination_and_caching():
    print("\n--- Testing Pagination and Caching ---")
    # 1. Create some movies
    for i in range(15):
        requests.post(f"{BASE_URL}/movies", json={
            "title": f"Movie {i}",
            "year": 2000 + i,
            "genre": "action"
        })
    
    # 2. Test Default Pagination (limit=10)
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/movies")
    duration_1 = time.time() - start_time
    data = response.json()
    print(f"Request 1 (Default): Got {len(data)} items. Time: {duration_1:.4f}s")
    
    if len(data) == 10:
        print("SUCCESS: Default pagination limit works.")
    else:
        print(f"FAILURE: Expected 10 items, got {len(data)}")

    # 3. Test Caching (Hit same endpoint)
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/movies")
    duration_2 = time.time() - start_time
    print(f"Request 2 (Cached?): Got {len(response.json())} items. Time: {duration_2:.4f}s")
    
    if duration_2 < duration_1:
        print("SUCCESS: Second request was faster (likely cached).")
    else:
        print("WARNING: Second request was not significantly faster.")

    # 4. Test Custom Pagination
    response = requests.get(f"{BASE_URL}/movies?skip=10&limit=5")
    data = response.json()
    print(f"Request 3 (Skip=10, Limit=5): Got {len(data)} items.")
    if len(data) == 5:
        print("SUCCESS: Custom pagination works.")
    else:
        print(f"FAILURE: Expected 5 items, got {len(data)}")

    # 4. Test Genre Filtering
    print("Request 4 (Genre=Action):")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/movies?genre=action")
    end_time = time.time()
    data = response.json()
    print(f"Request 4 (Genre=Action): Got {len(data)} items. Time: {end_time - start_time:.4f}s")
    
    if len(data) > 0 and all(m['genre'] == 'action' for m in data):
        print("SUCCESS: Genre filtering works.")
    else:
        print(f"FAILURE: Expected action movies, got {len(data)} items or wrong genre.")

if __name__ == "__main__":
    # Ensure server is running before running this
    try:
        test_pagination_and_caching()
        test_dynamic_rating()
        # test_config_registration_disabled() # Commented out as it requires app restart/reload behavior
    except Exception as e:
        print(f"An error occurred: {e}")

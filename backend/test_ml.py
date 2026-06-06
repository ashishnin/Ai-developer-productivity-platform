import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

def fetch_github_users(count=5):
    """Fetch a list of GitHub users"""
    url = f"https://api.github.com/search/users?q=type:user&per_page={count}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to fetch GitHub users: {resp.status_code}")
        return []
    data = resp.json()
    users = []
    for item in data.get('items', []):
        users.append({
            'username': item['login'],
            'email': f"{item['login']}@example.com",  # placeholder
            'github_id': item['id']
        })
    return users

def register_user(user):
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": user['username'],
        "email": user['email'],
        "password": "Password123!",
        "role": "developer"
    }
    resp = requests.post(url, json=payload)
    if resp.status_code in (200, 201):
        print(f"Registered user {user['username']}")
        return resp.json()
    else:
        print(f"Failed to register {user['username']}: {resp.status_code} {resp.text}")
        return None

def login_user(username, password="Password123!"):
    url = f"{BASE_URL}/auth/login"
    # OAuth2 expects form data
    data = {
        'username': username,
        'password': password
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(url, data=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()['access_token']
    else:
        print(f"Failed to login {username}: {resp.status_code} {resp.text}")
        return None

def create_project(token, name="Test Project"):
    url = f"{BASE_URL}/projects"
    payload = {
        "name": name,
        "description": "Project for ML testing",
        "repo_link": "https://github.com/example/repo"
    }
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        return resp.json()['id']
    else:
        print(f"Failed to create project: {resp.status_code} {resp.text}")
        return None

def create_activity(token, project_id, module_name):
    url = f"{BASE_URL}/activity/manual"
    # Generate some synthetic data
    import random
    payload = {
        "project_id": project_id,
        "developer_name": "testdev",  # we could use the username
        "commit_count": random.randint(5, 50),
        "lines_added": random.randint(100, 2000),
        "lines_deleted": random.randint(50, 500),
        "files_modified": random.randint(2, 20),
        "bug_count": random.randint(0, 10),
        "module_name": module_name
    }
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        print(f"  Created activity for module {module_name}")
        return resp.json()
    else:
        print(f"Failed to create activity: {resp.status_code} {resp.text}")
        return None

def predict_risk(token, module_name):
    url = f"{BASE_URL}/ai/predict-risk"
    params = {'module_name': module_name}
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.post(url, params=params, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"Failed to predict risk: {resp.status_code} {resp.text}")
        return None

def main():
    print("Fetching GitHub users...")
    users = fetch_github_users(count=3)
    if not users:
        print("Using fallback users")
        users = [
            {'username': 'torvalds', 'email': 'torvalds@example.com'},
            {'username': 'gaearon', 'email': 'gaearon@example.com'},
            {'username': 'sharkdp', 'email': 'sharkdp@example.com'}
        ]

    for user in users:
        print(f"\nProcessing user: {user['username']}")
        # Register
        reg = register_user(user)
        if not reg:
            # Maybe already exists, try to login anyway
            pass
        # Login
        token = login_user(user['username'])
        if not token:
            print("  Skipping due to login failure")
            continue
        # Create project
        project_id = create_project(token, f"{user['username']}'s Project")
        if not project_id:
            print("  Skipping due to project creation failure")
            continue
        # Create activity for a module
        module = "auth"
        activity = create_activity(token, project_id, module)
        if not activity:
            print("  Skipping due to activity creation failure")
            continue
        # Predict risk
        prediction = predict_risk(token, module)
        if prediction:
            print(f"  Risk prediction for module '{module}':")
            print(f"    Risk level: {prediction['risk_level']}")
            print(f"    Risk score: {prediction['risk_score']}")
            print(f"    Factors: {', '.join(prediction['factors'])}")
            print(f"    Recommendation: {prediction['recommendation']}")
        else:
            print("  Failed to get prediction")
        # Small delay to avoid rate limiting
        time.sleep(0.5)

if __name__ == '__main__':
    main()
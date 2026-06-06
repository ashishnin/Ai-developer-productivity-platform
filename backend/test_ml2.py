import requests
import json
import sys
import time
import random
import string

BASE_URL = "http://localhost:8000"

def random_suffix(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

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
            'github_id': item['id']
        })
    return users

def register_user(user):
    suffix = random_suffix()
    email = f"{user['username']}_{suffix}@example.com"
    user['email'] = email  # store for later login
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": user['username'],
        "email": email,
        "password": "Password123!",
        "role": "developer"
    }
    resp = requests.post(url, json=payload)
    if resp.status_code in (200, 201):
        print(f"Registered user {user['username']} with email {email}")
        return resp.json()
    else:
        print(f"Failed to register {user['username']}: {resp.status_code} {resp.text}")
        return None

def login_user(username, email, password="Password123!"):
    url = f"{BASE_URL}/auth/login"
    data = {
        'username': email,  # OAuth2 expects email as username field
        'password': password
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(url, data=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()['access_token']
    else:
        print(f"Failed to login {username} ({email}): {resp.status_code} {resp.text}")
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
    import random
    payload = {
        "project_id": project_id,
        "developer_name": "testdev",
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
            {'username': 'torvalds'},
            {'username': 'gaearon'},
            {'username': 'sharkdp'}
        ]

    for user in users:
        print(f"\nProcessing user: {user['username']}")
        # Register
        reg = register_user(user)
        if not reg:
            print("  Skipping due to registration failure")
            continue
        # Login
        token = login_user(user['username'], user['email'])
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
        # Small delay
        time.sleep(0.5)

if __name__ == '__main__':
    main()
import requests
import json
import time
import random

BASE_URL = "http://localhost:8000"

def register_user(username, email, password, role):
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    resp = requests.post(url, json=payload)
    if resp.status_code in (200, 201):
        print(f"Registered {role} {username}")
        return resp.json()
    else:
        # maybe already exists
        print(f"Failed to register {username}: {resp.status_code} {resp.text}")
        return None

def login_user(email, password):
    url = f"{BASE_URL}/auth/login"
    data = {
        'username': email,
        'password': password
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(url, data=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()['access_token']
    else:
        print(f"Failed to login {email}: {resp.status_code} {resp.text}")
        return None

def create_project(token, name, description="Sample project"):
    url = f"{BASE_URL}/projects"
    payload = {
        "name": name,
        "description": description,
        "repo_link": "https://github.com/example/repo"
    }
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        return resp.json()['id']
    else:
        print(f"Failed to create project: {resp.status_code} {resp.text}")
        return None

def create_activity(token, project_id, developer_name, module_name, commit_count, lines_added, lines_deleted, files_modified, bug_count):
    url = f"{BASE_URL}/activity/manual"
    payload = {
        "project_id": project_id,
        "developer_name": developer_name,
        "commit_count": commit_count,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "files_modified": files_modified,
        "bug_count": bug_count,
        "module_name": module_name
    }
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        print(f"Failed to create activity: {resp.status_code} {resp.text}")
        return None

def main():
    # Define users
    users = [
        {"username": "devuser", "email": "devuser@example.com", "password": "DevPass123!", "role": "developer"},
        {"username": "mgruser", "email": "mgruser@example.com", "password": "MgrPass123!", "role": "manager"}
    ]

    tokens = {}
    for user in users:
        print(f"\nProcessing {user['role']}: {user['username']}")
        # Register (ignore if exists)
        reg = register_user(user['username'], user['email'], user['password'], user['role'])
        # Login
        token = login_user(user['email'], user['password'])
        if not token:
            print(f"  Cannot proceed for {user['username']}")
            continue
        tokens[user['username']] = token
        # Create project
        proj_name = f"{user['username']}'s Project"
        project_id = create_project(token, proj_name, f"Project for {user['role']}")
        if not project_id:
            print(f"  Failed to create project for {user['username']}")
            continue
        print(f"  Created project ID: {project_id}")
        # Create some activities
        modules = ["auth", "api", "ui", "database", "utils"]
        for i, module in enumerate(modules):
            # Vary the data to create interesting metrics
            commit_count = random.randint(5, 30)
            lines_added = random.randint(100, 1500)
            lines_deleted = random.randint(50, 800)
            files_modified = random.randint(2, 15)
            bug_count = random.randint(0, 5)
            act = create_activity(
                token, project_id, user['username'], module,
                commit_count, lines_added, lines_deleted, files_modified, bug_count
            )
            if act:
                print(f"    Activity {i+1} for module {module}: commits={commit_count}, lines=+{lines_added}/-{lines_deleted}, files={files_modified}, bugs={bug_count}")
            else:
                print(f"    Failed to create activity for module {module}")
            time.sleep(0.1)  # be gentle

    print("\nSample data loading complete.")
    print("You can now login to the website with:")
    for user in users:
        print(f"  {user['username']} / {user['password']} ({user['role']})")

if __name__ == '__main__':
    main()
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
    print("Adding 4 developers under mgruser...")

    # First, ensure mgruser exists and get token
    mgr_token = login_user("mgruser@example.com", "MgrPass123!")
    if not mgr_token:
        print("ERROR: Cannot login as mgruser. Please run load_sample_data.py first.")
        return

    # Get mgruser's project (should be ID 5 from previous run)
    # Let's verify by getting projects
    projects_resp = requests.get(f"{BASE_URL}/projects",
                               headers={'Authorization': f'Bearer {mgr_token}'})
    if projects_resp.status_code == 200:
        projects = projects_resp.json()
        if projects:
            mgr_project_id = projects[0]['id']  # Take first project
            print(f"Using mgruser's project ID: {mgr_project_id}")
        else:
            # Create a team project for mgruser
            mgr_project_id = create_project(mgr_token, "Team Project", "Project managed by mgruser with team contributions")
            if not mgr_project_id:
                print("ERROR: Failed to create project for mgruser")
                return
            print(f"Created mgruser's team project ID: {mgr_project_id}")
    else:
        print("ERROR: Failed to fetch projects for mgruser")
        return

    # Define 4 developers to add under mgruser
    developers = [
        {"username": "dev1", "email": "dev1@example.com", "password": "DevPass123!"},
        {"username": "dev2", "email": "dev2@example.com", "password": "DevPass123!"},
        {"username": "dev3", "email": "dev3@example.com", "password": "DevPass123!"},
        {"username": "dev4", "email": "dev4@example.com", "password": "DevPass123!"}
    ]

    dev_tokens = {}

    # Register and login each developer
    for dev in developers:
        print(f"\nProcessing developer: {dev['username']}")
        # Register (ignore if exists)
        reg = register_user(dev['username'], dev['email'], dev['password'], "developer")
        # Login
        token = login_user(dev['email'], dev['password'])
        if not token:
            print(f"  Cannot proceed for {dev['username']}")
            continue
        dev_tokens[dev['username']] = token
        print(f"  Logged in as {dev['username']}")

    # Define modules and activity patterns for each developer
    modules = ["auth", "api", "ui", "database", "utils"]

    # Have each developer contribute activities to mgruser's project
    for dev_name, token in dev_tokens.items():
        print(f"\nAdding activities for {dev_name} to mgruser's project...")

        # Create 3-5 activities per developer across different modules
        num_activities = random.randint(3, 5)
        selected_modules = random.sample(modules, min(num_activities, len(modules)))

        for i, module in enumerate(selected_modules):
            # Generate realistic activity data
            commit_count = random.randint(10, 40)
            lines_added = random.randint(200, 2000)
            lines_deleted = random.randint(100, 800)
            files_modified = random.randint(3, 20)
            bug_count = random.randint(0, 8)

            act = create_activity(
                token, mgr_project_id, dev_name, module,
                commit_count, lines_added, lines_deleted, files_modified, bug_count
            )
            if act:
                print(f"    Activity {i+1} for module {module}: commits={commit_count}, lines=+{lines_added}/-{lines_deleted}, files={files_modified}, bugs={bug_count}")
            else:
                print(f"    Failed to create activity for module {module}")
            time.sleep(0.1)  # be gentle

    print("\nTeam data loading complete.")
    print("You can now login to the website as:")
    print(f"  mgruser / MgrPass123! (manager)")
    for dev in developers:
        print(f"  {dev['username']} / {dev['password']} (developer)")
    print("\nWhen logged in as mgruser, you will see:")
    print("- All activities from your team members on your projects")
    print("- Team productivity metrics in the dashboard")
    print("- Risk analysis for modules contributed by your team")
    print("- AI insights based on team activity")

if __name__ == '__main__':
    main()
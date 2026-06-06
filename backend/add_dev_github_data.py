import requests
import json
import time
import random

BASE_URL = "http://localhost:8000"

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

def get_projects(token):
    url = f"{BASE_URL}/projects"
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"Failed to get projects: {resp.status_code} {resp.text}")
        return []

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

def fetch_github_user_data(username):
    """Fetch real GitHub user data to base activity on"""
    url = f"https://api.github.com/users/{username}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"  Could not fetch GitHub data for {username}: {resp.status_code}")
        return None

def generate_activity_from_github(dev_github_data, module_name):
    """Generate realistic activity data based on GitHub user stats"""
    if not dev_github_data:
        # Fallback to random data
        return {
            'commit_count': random.randint(10, 50),
            'lines_added': random.randint(200, 2000),
            'lines_deleted': random.randint(100, 800),
            'files_modified': random.randint(3, 20),
            'bug_count': random.randint(0, 8)
        }

    # Use GitHub data to influence activity (more realistic)
    public_repos = dev_github_data.get('public_repos', 10)
    followers = dev_github_data.get('followers', 0)

    # Base activity on repo/follower count (more active users = more commits)
    commit_base = min(50, max(5, (public_repos * 2) + (followers // 10)))
    commit_count = random.randint(int(commit_base * 0.5), int(commit_base * 1.5))

    # Lines of code roughly related to repo count
    lines_base = min(3000, max(200, public_repos * 150))
    lines_added = random.randint(int(lines_base * 0.3), int(lines_base * 1.2))
    lines_deleted = random.randint(int(lines_added * 0.1), int(lines_added * 0.5))

    # Files modified related to activity level
    files_base = min(25, max(3, public_repos // 2))
    files_modified = random.randint(int(files_base * 0.5), int(files_base * 2))

    # Bug count - somewhat random but influenced by activity
    bug_count = random.randint(0, min(10, commit_count // 5))

    return {
        'commit_count': commit_count,
        'lines_added': lines_added,
        'lines_deleted': lines_deleted,
        'files_modified': files_modified,
        'bug_count': bug_count
    }

def main():
    print("Adding GitHub-based activity data for dev1-dev4...")

    developers = [
        {"username": "dev1", "email": "dev1@example.com", "password": "DevPass123!"},
        {"username": "dev2", "email": "dev2@example.com", "password": "DevPass123!"},
        {"username": "dev3", "email": "dev3@example.com", "password": "DevPass123!"},
        {"username": "dev4", "email": "dev4@example.com", "password": "DevPass123!"}
    ]

    modules = ["auth", "api", "ui", "database", "utils"]

    for dev in developers:
        print(f"\nProcessing {dev['username']}...")

        # Login as developer
        token = login_user(dev['email'], dev['password'])
        if not token:
            print(f"  Cannot proceed for {dev['username']}")
            continue

        # Get or create project for this developer
        projects = get_projects(token)
        if projects:
            # Use existing project (take first one)
            project_id = projects[0]['id']
            project_name = projects[0]['name']
            print(f"  Using existing project: {project_name} (ID: {project_id})")
        else:
            # Create new project
            project_name = f"{dev['username']}'s GitHub Project"
            project_id = create_project(token, project_name, f"Project for {dev['username']} with GitHub-based activity")
            if not project_id:
                print(f"  Failed to create project for {dev['username']}")
                continue
            print(f"  Created project: {project_name} (ID: {project_id})")

        # Fetch GitHub data for this username
        github_data = fetch_github_user_data(dev['username'])
        if github_data:
            print(f"  GitHub data: {github_data.get('public_repos', 0)} repos, {github_data.get('followers', 0)} followers")
        else:
            print(f"  Using simulated data for {dev['username']}")

        # Create 3-5 activities across different modules
        num_activities = random.randint(3, 5)
        selected_modules = random.sample(modules, min(num_activities, len(modules)))

        print(f"  Creating {len(selected_modules)} activities...")

        for i, module in enumerate(selected_modules):
            # Generate activity data based on GitHub stats
            activity_data = generate_activity_from_github(github_data, module)

            act = create_activity(
                token, project_id, dev['username'], module,
                activity_data['commit_count'],
                activity_data['lines_added'],
                activity_data['lines_deleted'],
                activity_data['files_modified'],
                activity_data['bug_count']
            )

            if act:
                print(f"    Activity {i+1} for {module}:")
                print(f"      Commits: {activity_data['commit_count']}")
                print(f"      Lines: +{activity_data['lines_added']}/-{activity_data['lines_deleted']}")
                print(f"      Files: {activity_data['files_modified']}")
                print(f"      Bugs: {activity_data['bug_count']}")
            else:
                print(f"    Failed to create activity for module {module}")

            time.sleep(0.1)  # be gentle with API

        # Small delay between developers
        time.sleep(0.5)

    print("\nGitHub-based activity data loading complete.")
    print("You can now login to the website as any dev1-dev4 to see their GitHub-inspired activity data.")
    print("Credentials: devX@example.com / DevPass123!")

if __name__ == '__main__':
    main()
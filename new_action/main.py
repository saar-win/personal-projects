from email import header
import os
import yaml
import requests
import subprocess
import uuid
from requests.auth import HTTPBasicAuth


def main():
    '''
    '''
    # yaml_file = load_yaml(os.getenv('INPUT_FILE'))

    # print(yaml_file)

    # branch_name = f"test_{uuid.uuid4().hex[:6]}"

    # git_actions(branch_name)

    # open_git_pr(branch_name="test_123", service_name = "test", repo_name = os.environ.get("GITHUB_REPOSITORY"))
    open_git_pr(branch_name="test_123", service_name = "test", repo_name = "saar-win/personal-projects")

def load_yaml(file_path):
    '''
    '''
    yaml_file = yaml.safe_load(open(file_path))
    return yaml_file

def git_actions(branch_name):
    '''
    '''
    commit_msg = "test"
    subprocess.run(f"git checkout -b {branch_name}", shell=True)
    subprocess.run("touch file.txt", shell=True)
    subprocess.run("git add -A", shell=True)
    subprocess.run(f"git commit -am {commit_msg}", shell=True)
    subprocess.run(f"git push --set-upstream origin {branch_name}", shell=True)
    # return

def open_git_pr(branch_name, service_name, repo_name):
    '''
    '''
    headers = {
        "Accept": "application/vnd.github.v3+json"
        }
    json={
        'title': f'new changes in services, {service_name}',
        'body': f'New service {service_name}',
        'head': f'{branch_name}',
        'base': 'main'
    }
    res = requests.post('https://api.github.com/repos/{}/pulls'.format(repo_name),
        json = json,
        headers = headers,
        auth = HTTPBasicAuth(os.getenv('INPUT_ACTIONS_ACCESS_USERNAME'), os.getenv('INPUT_ACTIONS_ACCESS_KEY'))
        )
    print(res.text)

    if res.ok:
        return res.json()
    else:
        raise Exception(f"Error creating PR to {repo_name}")

if __name__ == '__main__':
    main()
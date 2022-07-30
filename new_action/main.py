from email import header
import os
import yaml
import requests
import subprocess
import uuid

def main():
    '''
    '''
    yaml_file = load_yaml(os.getenv('INPUT_FILE'))
    print(yaml_file)
    branch_name = f"test_{uuid.uuid4()}"
    git_actions(branch_name)
    open_git_pr(branch_name)

def load_yaml(file_path):
    '''
    '''
    yaml_file = yaml.safe_load(open(file_path))
    return yaml_file

def git_actions(branch_name):
    '''
    '''

    subprocess.run(f"git checkout -b {branch_name}", shell=True)
    subprocess.run("touch file.txt", shell=True)
    subprocess.run("git add -A", shell=True)
    subprocess.run("git commit -am test", shell=True)
    subprocess.run(f"git push --set-upstream origin {branch_name}", shell=True)
    # return

def open_git_pr(branch_name):
    '''
    '''
    service_name = "test"
    token = {os.environ('INPUT_ACTIONS_ACCESS_USERNAME') + ":" + os.environ('INPUT_ACTIONS_ACCESS_KEY')}
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    json={
        'title': 'New Action',
        'body': f'New service {service_name}',
        'head': f'{branch_name}',
        'base': 'master'
    }
    res = requests.post('https://api.github.com/repos/saar-win/personal-projects/pulls', json=json, headers=headers)
    print(res.text)

    if res.ok:
        return res.json()
    else:
        raise Exception("Error creating PR")

if __name__ == '__main__':
    main()
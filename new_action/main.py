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
    git_actions()
    open_git_pr()

def load_yaml(file_path):
    '''
    '''
    yaml_file = yaml.safe_load(open(file_path))
    return yaml_file

def git_actions():
    '''
    '''
    subprocess.run("git checkout -b test", shell=True)
    subprocess.run("touch file.txt", shell=True)
    subprocess.run("git add -A", shell=True)
    subprocess.run("git commit -am test", shell=True)
    subprocess.run("git push --set-upstream origin test", shell=True)
    # return

def open_git_pr():
    '''
    '''
    service_name = "test"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    res = requests.post('https://api.github.com/repos/saar-win/personal-projects/pulls',
        json={
            'title': 'New Action',
            'body': f'New service {service_name}',
            'head': f'test_{uuid.uuid4()}',
            'base': 'master'
        },
    headers=headers
    )
    print(res.text)
    if res is not None:
        return res.json()
    else:
        raise Exception("Error creating PR")

if __name__ == '__main__':
    main()
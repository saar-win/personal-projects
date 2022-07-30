import os
import yaml
import requests
import subprocess

def main():
    '''
    '''
    yaml_file = load_yaml(os.getenv('INPUT_FILE'))
    print(yaml_file)
    git_actions()
    open_git_pr(github_repository="saar-win/personal-projects")

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

def open_git_pr(github_repository):
    '''
    '''
    service_name = "test"
    res = requests.post('https://api.github.com/repos/{}/pulls'.format(github_repository),
        json={
            'title': 'New Action',
            'body': f'New service {service_name}',
            'head': 'test',
            'base': 'master'
        }
    )
    print(res.text)
    if res is not None:
        return res.json()
    else:
        raise Exception("Error creating PR")

if __name__ == '__main__':
    main()
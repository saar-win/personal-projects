import os
import yaml
import uuid
import json
import requests
import subprocess
from requests.auth import HTTPBasicAuth

def main():
    '''
    '''
    # Load yaml file
    yaml_file = load_yaml(os.getenv('INPUT_FILE'))

    # create random branch name
    branch_name = f"test_{uuid.uuid4().hex[:6]}"

    templates = create_template(yaml_file, os.getenv("INPUT_COMPUTE_POWER_FILE"), os.getenv("INPUT_FLAG_FILE"))

    # open branch add files
    git_actions(branch_name)

    # open PR
    open_git_pr(branch_name, service_name = yaml_file['name'], repo_name = os.getenv("GITHUB_REPOSITORY"))

def load_flag_features(flag_file):
    '''
    '''
    with open(flag_file, 'r') as f:
        obj = json.load(f)
    return obj


def load_yaml(file_path):
    '''
    '''
    yaml_file = yaml.safe_load(open(file_path))
    return yaml_file['service']

def create_template(_object, path_compute_power_file, flag_file):
    '''
    '''
    feature_flag = load_flag_features(flag_file)

    # with open('templates/Deployment.yaml', 'r') as f:
    #     template = yaml.safe_load(f)

    # read the existing compute power files
    compute_power_file = yaml.safe_load(open(path_compute_power_file))
##################################################################################################################################
    if _object['templates']['deployment'] and feature_flag['deployment']:

        if feature_flag['deployment']['resources']['requests']['cpu'] and _object['resources']['requests']['cpu']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('requests') != None:
                    compute_power_file['computepower']['services'][_object['name']]['requests']['cpu'] = _object['resources']['requests']['cpu']
                elif compute_power_file['computepower']['services'][_object['name']].get('requests') == None:
                    compute_power_file['computepower']['services'][_object['name']]['requests'] = {}
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "requests": {
                    'cpu': _object['resources']['requests']['cpu']
                    }
                })
        with open('compute-power-file.yml', 'w') as f:
            f.write(yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False))
            f.close()
##################################################################################################################################
        if feature_flag['deployment']['resources']['requests']['memory'] and _object['resources']['requests']['memory']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('requests') != None:
                    compute_power_file['computepower']['services'][_object['name']]['requests']['memory'] = _object['resources']['requests']['memory']
                elif compute_power_file['computepower']['services'][_object['name']].get('requests') == None:
                    compute_power_file['computepower']['services'][_object['name']]['requests'] = {}
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "requests": {
                    'memory': _object['resources']['requests']['memory']
                    }
                })
        with open('compute-power-file.yml', 'w') as f:
            f.write(yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False))
            f.close()
##################################################################################################################################
        if feature_flag['deployment']['resources']['limits']['cpu'] and _object['resources']['limits']['cpu']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('limits') != None:
                    compute_power_file['computepower']['services'][_object['name']]['limits']['cpu'] = _object['resources']['limits']['cpu']
                elif compute_power_file['computepower']['services'][_object['name']].get('limits') == None:
                    compute_power_file['computepower']['services'][_object['name']]['limits'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['limits']['cpu'] = _object['resources']['limits']['cpu']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "limits": {
                    'cpu': _object['resources']['limits']['cpu']
                    }
                })
        with open('compute-power-file.yml', 'w') as f:
            f.write(yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False))
            f.close()
    ##################################################################################################################################
        if feature_flag['deployment']['resources']['limits']['memory'] and _object['resources']['limits']['memory']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('limits') != None:
                    compute_power_file['computepower']['services'][_object['name']]['limits']['memory'] = _object['resources']['limits']['memory']
                if compute_power_file['computepower']['services'][_object['name']].get('limits') == None:
                    compute_power_file['computepower']['services'][_object['name']]['limits'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['limits']['memory'] = _object['resources']['limits']['memory']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "limits": {
                    'memory': _object['resources']['limits']['memory']
                    }
                })
        with open('compute-power-file.yml', 'w') as f:
            f.write(yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False))
            f.close()
##################################################################################################################################

#     if _object['templates']['deployment'] and feature_flag['deployment']:
#         env_vars = template['spec']['template']['spec']['containers'][0]['env']
#         # print(env_vars)
#         # print(_object['envs'])

# ########################################################################################

#     if _object['templates']['secrets'] and feature_flag['secrets']:
#         with open('templates/secret.yaml', 'r') as f:
#             template = yaml.safe_load(f)
#         secret_vars = template['data']
#         print(secret_vars)

# ########################################################################################

#     if _object['templates']['service'] and feature_flag['service']:
#         with open('templates/service.yaml', 'r') as f:
#             template = yaml.safe_load(f)
#         service = template['data']
#         print(service)

# ########################################################################################

#     if _object['templates']['configmap'] and feature_flag['configmap']:
#         with open('templates/configmap.yaml', 'r') as f:
#             template = yaml.safe_load(f)
#         configmap = template['data']
#         print(configmap)
#     return ""

########################################################################################

def git_actions(branch_name):
    '''
    '''
    commit_msg = "test"
    subprocess.run(f'git config --global user.email "saar1122@gmail.com"', shell=True)
    subprocess.run(f'git config --global user.name "saar-win"', shell=True)
    subprocess.run(f'chown -R runner .', shell=True)
    subprocess.run(f'git checkout -b {branch_name}', shell=True)
    subprocess.run(f'git commit -am {commit_msg}', shell=True)
    subprocess.run(f'git push --set-upstream origin {branch_name}', shell=True)
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

    if res.ok:
        return True
    else:
        print(res.json())
        raise Exception(f"Error creating PR to {repo_name}")

if __name__ == '__main__':
    main()
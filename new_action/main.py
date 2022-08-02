import os
import git
import yaml
import uuid
import json
import shutil
import requests
import subprocess
from requests.auth import HTTPBasicAuth


def main():
    '''
    a list of env var that this script has to get:
    GIT_TO_CLONE: # https://github.com/saar-win/personal-projects.git
    INPUT_COMPUTE_POWER_FILE # path to the compute power file # '/tmp/changes/new_action/compute-power-file.yml'
    INPUT_FLAG_FILE: # path to the flag file # '/tmp/changes/new_action/flag.json'
    WORKING_BRANCH # on which branch the changes will be made # main
    INPUT_FILE # for every service # $GITHUB_WORKSPACE/<SERVICE_NAME>.yml
    REPO_NAME # for every service # saar-win/personal-projects
    '''
    # Load yaml file
    yaml_file = load_yaml(os.getenv('INPUT_FILE'))

    # initialize git repo
    git_to_clone = f"https://{os.getenv('INPUT_ACTIONS_ACCESS_KEY')}@github.com/{os.getenv('INPUT_REPO_NAME')}"
    working_branch = "main"
    repo = github("clone", "/tmp" ,git_to_clone, working_branch, "", "")

    # set the account
    github("set_account", "", "", "", repo, "")

    # create new branch
    branch_name = f"services/{yaml_file['service']['name']}_{uuid.uuid4().hex[:6]}"
    new_branch = github("new_branch", "" ,"", branch_name, repo, "")

    # templating the files
    templates = create_template(yaml_file['service'], os.getenv("INPUT_COMPUTE_POWER_FILE"), os.getenv("INPUT_FLAG_FILE"))

    # add files to branch
    commit_msg = f"This is a changes for the service {yaml_file['service']['name']}"
    changed_files = github("add_files_push", "/tmp" , "", branch_name, repo, commit_msg)

    # open PR
    ans = open_git_pr(branch_name, working_branch, yaml_file['service']['name'], git_to_clone, changed_files)

    if ans:
        print("PR created")

def github(action, path_to_clone ,git_to_clone, branch_name, repo, commit_msg):
    '''
    '''
    # clone the repository
    if action == "clone":
        os.chdir(path_to_clone)
        if os.path.isdir(path_to_clone + "/changes"):
            shutil.rmtree(path_to_clone + "/changes")
        repo = git.Repo.clone_from(git_to_clone, path_to_clone + "/changes")
        repo.git.checkout(branch_name)
        return repo

    # git set account
    if action == "set_account":
        repo.config_writer().set_value("user", "name", os.getenv('INPUT_ACTIONS_ACCESS_USERNAME')).release()
        repo.config_writer().set_value("user", "email", "saar1122@gmail.com").release()

    # create new branch
    if action == "new_branch":
        repo = repo.git.checkout("-b", branch_name)

    # add the files and push
    if action == "add_files_push":
        repo.git.add("-A")
        changed_files = [ repo.git.diff(repo.head.commit, name_only=True) ]
        repo.git.commit("-m", commit_msg)
        os.environ['GIT_USERNAME'] = os.getenv('INPUT_ACTIONS_ACCESS_USERNAME')
        os.environ['GIT_PASSWORD'] = os.getenv('INPUT_ACTIONS_ACCESS_KEY')
        repo.git.push("origin", branch_name)
        return changed_files

def load_yaml(file_path):
    '''
    '''
    # load the yaml file
    yaml_file = yaml.safe_load(open(file_path))
    return yaml_file

def load_flag_features(flag_file_path):
    '''
    '''
    # load the features flag file
    flag_file = open(flag_file_path, 'r')
    return json.loads(flag_file.read())

def create_template(_object, compute_power_file_path, flag_file_path):
    '''
    '''
    # load the features flag file
    feature_flag = load_flag_features(flag_file_path)

    # read the existing compute power files
    compute_power_file = load_yaml(compute_power_file_path)

##################################################################################################################################
    if _object['templates']['deployment'] and feature_flag.get('deployment'):
        if feature_flag['deployment']['resources']['requests']['cpu'] and _object['resources']['requests']['cpu']:
            if compute_power_file['computepower'].get('services') == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('resources_requests') != None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_requests']['cpu'] = _object['resources']['requests']['cpu']
                elif compute_power_file['computepower']['services'][_object['name']].get('resources_requests') == None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_requests'] = {}
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "resources_requests": {
                    'cpu': _object['resources']['requests']['cpu']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        if feature_flag['deployment']['resources']['requests']['memory'] and _object['resources']['requests']['memory']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('resources_requests') != None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_requests']['memory'] = _object['resources']['requests']['memory']
                elif compute_power_file['computepower']['services'][_object['name']].get('resources_requests') == None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_requests'] = {}
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "resources_requests": {
                    'memory': _object['resources']['requests']['memory']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        if feature_flag['deployment']['resources']['limits']['cpu'] and _object['resources']['limits']['cpu']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('resources_limits') != None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_limits']['cpu'] = _object['resources']['limits']['cpu']
                elif compute_power_file['computepower']['services'][_object['name']].get('resources_limits') == None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_limits'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['resources_limits']['cpu'] = _object['resources']['limits']['cpu']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "resources_limits": {
                    'cpu': _object['resources']['limits']['cpu']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
    ##################################################################################################################################
        if feature_flag['deployment']['resources']['limits']['memory'] and _object['resources']['limits']['memory']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('resources_limits') != None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_limits']['memory'] = _object['resources']['limits']['memory']
                if compute_power_file['computepower']['services'][_object['name']].get('resources_limits') == None:
                    compute_power_file['computepower']['services'][_object['name']]['resources_limits'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['resources_limits']['memory'] = _object['resources']['limits']['memory']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "resources_limits": {
                    'memory': _object['resources']['limits']['memory']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
    ##################################################################################################################################
        if feature_flag['hpa']['minReplicas'] and _object['hpa']['minReplicas']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') != None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['minReplicas'] = _object['hpa']['minReplicas']
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') == None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['minReplicas'] = _object['hpa']['minReplicas']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "hpa": {
                    'minReplicas': _object['hpa']['minReplicas']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        if feature_flag['hpa']['maxReplicas'] and _object['hpa']['maxReplicas']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') != None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['maxReplicas'] = _object['hpa']['maxReplicas']
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') == None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['maxReplicas'] = _object['hpa']['maxReplicas']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "hpa": {
                    'maxReplicas': _object['hpa']['maxReplicas']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        if feature_flag['hpa']['averageMEMORY'] and _object['hpa']['averageMEMORY']:
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') != None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['averageMEMORY'] = _object['hpa']['averageMEMORY']
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') == None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['averageMEMORY'] = _object['hpa']['averageMEMORY']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "hpa": {
                    'averageMEMORY': _object['hpa']['averageMEMORY']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        if feature_flag['hpa']['averageCPU'] and _object.get('hpa').get('averageCPU'):
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') != None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['averageCPU'] = _object['hpa']['averageCPU']
                if compute_power_file['computepower']['services'][_object['name']].get('hpa') == None:
                    compute_power_file['computepower']['services'][_object['name']]['hpa'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['hpa']['averageCPU'] = _object['hpa']['averageCPU']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "hpa": {
                    'averageCPU': _object['hpa']['averageCPU']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        if feature_flag['pdb']['minAvailable'] and _object.get('pdb').get('minAvailable'):
            if compute_power_file['computepower']['services'] == None:
                compute_power_file['computepower']['services'] = {}
            if compute_power_file['computepower']['services'].get(_object['name']) != None:
                if compute_power_file['computepower']['services'][_object['name']].get('pdb') != None:
                    compute_power_file['computepower']['services'][_object['name']]['pdb']['minAvailable'] = _object['pdb']['minAvailable']
                if compute_power_file['computepower']['services'][_object['name']].get('pdb') == None:
                    compute_power_file['computepower']['services'][_object['name']]['pdb'] = {}
                    compute_power_file['computepower']['services'][_object['name']]['pdb']['minAvailable'] = _object['pdb']['minAvailable']
            elif compute_power_file['computepower']['services'].get(_object['name']) == None:
                to_append = compute_power_file['computepower']['services'][_object['name']] = {}
                to_append.update({ "pdb": {
                    'minAvailable': _object['pdb']['minAvailable']
                    }
                })
        with open(compute_power_file_path, 'w') as f:
            file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
            f.write(file)
            f.close()
##################################################################################################################################
        # if feature_flag['forks']['numberOfForks'] and _object['forks']['numberOfForks']:
        #     if compute_power_file['computepower']['services'] == None:
        #         compute_power_file['computepower']['services'] = {}
        #     if compute_power_file['computepower']['services'].get(_object['name']) != None:
        #         if compute_power_file['computepower']['services'][_object['name']].get('forks') != None:
        #             compute_power_file['computepower']['services'][_object['name']]['forks']['numberOfForks'] = _object['forks']['numberOfForks']
        #         if compute_power_file['computepower']['services'][_object['name']].get('forks') == None:
        #             compute_power_file['computepower']['services'][_object['name']]['forks'] = {}
        #             compute_power_file['computepower']['services'][_object['name']]['forks']['numberOfForks'] = _object['forks']['numberOfForks']
        #     elif compute_power_file['computepower']['services'].get(_object['name']) == None:
        #         to_append = compute_power_file['computepower']['services'][_object['name']] = {}
        #         to_append.update({ "forks": {
        #             'numberOfForks': _object['forks']['numberOfForks']
        #             }
        #         })
        # with open(compute_power_file_path, 'w') as f:
        #     file = yaml.dump(compute_power_file, default_flow_style=False, sort_keys=False)
        #     f.write(file)
        #     f.close()
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
def open_git_pr(branch_name, working_branch, service_name, repo_name_url, changed_files):
    '''
    '''
    # flat the list
    changed_files = '\n'.join(changed_files)

    headers = { "Accept": "application/vnd.github.v3+json" }
    json={
        'title': f'new changes in services, {service_name}',
        'body': f'## New changes in files: \n {changed_files}',
        'head': branch_name,
        'base': working_branch
    }
    repo_name = repo_name_url.split("@github.com/")[1].split(".git")[0]
    res = requests.post(f'https://api.github.com/repos/{repo_name}/pulls',
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
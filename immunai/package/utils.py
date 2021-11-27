import redis, yaml, json, os
import requests, yaml, json

path = "/Users/saarwintrov/devel/releai/personal-projects-1/immunai"
files = os.listdir(path + "/objects/")


class Redis_actions:
    def __init__(self, host):
        self.host = host
        self.client = redis.Redis(host="redis_json_db", port=6379, decode_responses=True)

    def read(self, file_name):
        '''
        '''
        return json.loads(self.client.execute_command('JSON.GET', file_name))

    def write(self, file_name, content):
        '''
        '''
        obj = {
            'foo': 'bar'
            }
        self.client.execute_command('JSON.SET', file_name, '.', json.dumps(content))

class Actions:
    def read(file_name) -> dict:
        '''
        '''
        file = open(file_name, "r")
        return json.load(file)

    def write(file_name, content):
        '''
        '''
        file = open(path + "/objects/" + file_name + ".json", "w")
        return file.write(json.dumps(content))

def loaded_yaml():
    '''
    '''
    return yaml.load(open(f"{path}/input.yaml").read(),Loader=yaml.FullLoader)

def get_starwars():
    '''
    '''
    objs = []
    values_list = []
    types = []
    yaml = loaded_yaml()["input"]
    for req in yaml:
        types.append(req['type'])
        _type = req['type']
        url = f"https://swapi.dev/api/{_type}/{req['id']}"
        objs.append({
            "values" : json.loads(requests.get(url).text),
            "keys" : req['infoRequest']
        })
    for obj in objs:
        value_dict = {}
        for key, val in obj["values"].items():
            if key in obj["keys"]:
                value_dict[key] = val
        values_list.append(value_dict)
    for data, req in zip(values_list, yaml):
        name = data['name'].replace(" ", "_").lower()
        Actions.write(name, data)

def check_if_exist():
    '''
    '''
    if len(files) != 0:
        for file in files:
            os.remove(path + "/objects/" + file)
import os
from flask import Flask, jsonify
from package.utils import *

app = Flask(__name__)

path = "/Users/saarwintrov/devel/releai/personal-projects-1/immunai"
db = Redis_actions(os.environ["REDIS_JSON_DB"])
files = os.listdir(path + "/objects/")

@app.route("/write")
def write_to_redis():
    '''
    '''
    check_if_exist()
    get_starwars()
    for file in files:
        content = Actions.read(path + "/objects/" + file)
        db.write(file.split(".json")[0], content)
    return jsonify({ "message": "Done" }), 200

@app.route("/read")
def read_from_redis():
    '''
    '''
    data = []
    for file in files:
        content = db.read(file.split(".json")[0])
        data.append({ file.split(".json")[0]: content})
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
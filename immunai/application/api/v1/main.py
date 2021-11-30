import os
from flask import Flask, jsonify
from package.utils import *

app = Flask(__name__)

db = Redis_actions(os.environ["REDIS_IP_SERVER"])
path = f"{os.environ['FILE_PATH']}"

@app.route("/api/v1/write")
def write_to_redis():
    '''
    Get the object from the Starwars api
    write it to file
    write it to redis
    '''
    check_if_exist()
    get_starwars()
    files = os.listdir(path + "/objects/")
    for file in files:
        content = Actions.read(path + "/objects/" + file)
        db.write(file.split(".json")[0], content)
    return jsonify({ "message": "Done" }), 200

@app.route("/api/v1/read")
def read_from_redis():
    '''
    Read the object from redis json service
    '''
    data = []
    files = os.listdir(path + "/objects/")
    try:
        for file in files:
            content = db.read(file.split(".json")[0])
            data.append({ file.split(".json")[0]: content})
        return jsonify(data), 200
    except Exception:
        return jsonify({ "message": "Internal err" }), 500

if __name__ == '__main__':
    app.run(debug=True)
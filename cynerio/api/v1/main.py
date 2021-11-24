import json, os
from flask import Flask, request, jsonify
from package.utils import *

app = Flask(__name__)
_redis = Redis_actions(os.environ["REDIS_HOST"])

@app.route("/set", methods=["POST"] )
def write_to_redis():
    '''
    write to redis and returns 200
    '''
    try:
        if _redis.set(request.get_data().decode('utf-8')) == True:
            return jsonify({ "message": "Success" }), 200
    except Exception:
        return jsonify({ "message": "Something went wrong" }), 500

@app.route("/healthcheck", methods=["GET"] )
def healthz():
    '''
    healhcheck and returns 200
    '''
    return jsonify({ "status": "ok" }), 200

@app.route("/get/<_id>", methods=["GET"] )
def get_data(_id):
    '''
    get value from redis
    '''
    ans = _redis.get(_id)
    if ans != None:
        return jsonify({ _id: ans }), 200
    else:
        return jsonify({ "message": f"Something went wrong, something with your key: {_id}" }), 404

@app.route("/delete/<_id>", methods=["GET"] )
def delete_data(_id):
    '''
    get value from redis
    '''
    if _redis.delete(_id) != None:
        return jsonify({ "message": f"the key data deleted {_id}" }), 200
    else:
        return jsonify({ "message": "Something went wrong" }), 500

if __name__ == '__main__':
    app.run(debug=True)

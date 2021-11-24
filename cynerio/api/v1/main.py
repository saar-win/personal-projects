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
        if _redis.set_redis(request.get_data().decode('utf-8')) == True:
            return jsonify({ "message": "Success" }), 200
    except Exception:
        return jsonify({ "message": "Something went wrong" }), 500

@app.route("/healthcheck", methods=["GET"] )
def healthz():
    '''
    healhcheck and returns 200
    '''
    return { "status": "ok" }, 200

@app.route("/get/<_id>", methods=["GET"] )
def get_data(_id):
    '''
    get value from redis
    '''
    try:
        return jsonify({ _id: _redis.get_redis(_id) })
    except Exception:
        return jsonify({ "message": "Something went wrong" }), 500

if __name__ == '__main__':
    app.run(debug=True)

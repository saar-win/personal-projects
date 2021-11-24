import redis
import json, os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/set", methods=["POST"] )
def write_to_redis():
    '''
    write to redis and returns 200
    '''
    obj = json.loads(request.get_data().decode('utf-8'))
    r = redis_init()
    try:
        r.set(obj["id"], obj["data"])
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        print(e)
        return jsonify({ "message": str(e) }), 500

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
    r = redis_init()
    try:
        from_redis = r.get(_id).decode('utf-8')
        return jsonify({_id: from_redis})
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

def redis_init():
    '''
    init redis
    '''
    r = redis.Redis(host=os.environ["REDIS_HOST"], port=6379, db=0)
    return r

if __name__ == '__main__':
    app.run(debug=True)

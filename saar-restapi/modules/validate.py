from flask import request, jsonify
from functools import wraps

def auth_middleware():
    def _auth_middleware(f):
        @wraps(f)
        def middleware(*args, **kwargs):
            if request.is_json:
                return f(*args, **kwargs)
            else:
                return jsonify({ "error": "invalid content-type" }), 400

        return middleware

    return _auth_middleware
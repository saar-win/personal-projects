from contextlib import ExitStack
from flask import Flask, request, jsonify
from modules.validate import *
from modules.calc import *
from modules.utils import *

app = Flask(__name__)

@app.route('/api/v1/math/<action>',  methods=["POST"])
@auth_middleware()
@write_logs()
def main(action):
    '''
    Get the data from the user
    1. option to sum the numbers.
    2. option to sort the number.
    '''
    try:
        value = request.get_json()
        if request.is_json:
            if action == "sum":
                    return jsonify({ "sum": sum_fun(*value.values())}), 200

            elif action == "sort":
                    return jsonify({ "result": sort_fun(*value["data"]) }), 200

        else:
            return jsonify({ "message": "Not Found" }), 404
    except:
        return jsonify({ "error": "something when wrong" }), 500

if __name__ == '__main__':
    app.run(debug=True)

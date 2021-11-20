from flask import Flask, request
import json
from modules.validate import *
from modules.utils import *

app = Flask(__name__)

@app.route('/api/v1/audit',  methods=["GET", "POST"])
def router():
    '''
    route the requests
    '''
    if request.method == "POST":
        payload = request.get_data().decode('utf-8')
        _id = write_logs_to_db(json.loads(payload))
        return str(_id)

    if request.method == "GET":
        limit = int(request.args.get("limit", 100))
        converted_obj = read_logs_from_db(limit)
        return converted_obj

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/customer/v1", methods=["GET"] )
def send_hello_world():
    '''
    Returns to user Hello World!
    '''
    return { "message": "Hello World" }, 200


@app.route("/healthz", methods=["GET"] )
def healthz():
    '''
    Handling with other kinds of request
    '''
    return { "message": "success" }, 200

@app.route("/", methods=["GET"] )
def not_found():
    '''
    Handling with other kinds of request
    '''
    return { "message": "success" }, 200

if __name__ == '__main__':
    app.run(debug=True)

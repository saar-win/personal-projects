from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/devops")
def main():
    '''
    Returns the index.html
    '''
    return jsonify({ "message": "Oh My DevOps!!" }), 200

if __name__ == '__main__':
    app.run(debug=True)

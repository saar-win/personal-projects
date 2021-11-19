from flask import Flask, render_template, jsonify


app = Flask(__name__)

@app.route("/")
def index():
    '''
    Returns the index.html
    '''
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

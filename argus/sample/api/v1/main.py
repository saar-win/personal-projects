from flask import Flask, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route("/")
def index():
    '''
    Returns to index.html
    '''
    return render_template('index.html', data = times())

def times():
    '''
    Retruns worldwide times
    '''
    return {
        "TLV": datetime.now(tz=pytz.timezone('Asia/Jerusalem')).ctime(),
        "LON":  datetime.now(tz=pytz.timezone('Europe/London')).ctime(),
        "NY": datetime.now(tz=pytz.timezone('America/New_York')).ctime(),
    }

if __name__ == '__main__':
    app.run(debug=True)

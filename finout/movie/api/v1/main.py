from flask import Flask, jsonify
from package.utils import *
from package.calc import *
from flask_apscheduler import APScheduler


# defines flask app
app = Flask(__name__)
# defines the scheduler
scheduler = APScheduler()

def scheduleTask():
    '''
    schedule task for write the object data
    '''
    # get the obj from finout
    data = obj_from_finout()
    # write to file
    update_movie_storage(data)

# set the interval and start it
scheduler.add_job(id="scheduleTask", func=scheduleTask, trigger="interval", seconds=3)
scheduler.start()

@app.route('/api/v1/movie',  methods=["GET"])
def get_movie():
    '''
    returns a valid object, filtered 500 err
    '''
    # returns the object to the user after filtered
    return obj_from_finout(), 200

@app.route('/api/v1/last_movies',  methods=["GET"])
def last_movies():
    '''
    returns the last 10 movies
    '''
    # send to user the movie from the finout api
    result = last_ten_movies()

    # check if not empty file
    if result != None:
        return jsonify(result), 200
    else:
        return jsonify({ "message": "the storage file is empty" }), 500

@app.route('/api/v1/average',  methods=["GET"])
def get_average():
    '''
    returns the average hours of the movies
    '''
    # returns to the avarage time from all movies in obj
    result, number_of_movies = time_duration_average()

    # check if not empty file
    if result != None:
        return jsonify({ f"the everage of {number_of_movies} movies is": result }), 200
    else:
        return jsonify({ "message": "the storage file is empty" }), 500

if __name__ == '__main__':
    # scheduleTask()
    app.run(debug=True)
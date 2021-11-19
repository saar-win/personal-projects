import os
from package.utils import *

def time_duration_average():
    '''
    get durations from the object.
    returns the average of the durations
    and the number of the movies in file
    '''
    durations = []

    # check if the file exist or empty
    if not os.path.exists(storge_db) or os.stat(storge_db).st_size == 0:
        return None, None
    # read the file and get the duration
    movies = Object.read()

    # add the movie duration to an array
    for movie in movies["movies"]:
        durations.append(movie["duration"])
    result = sum(durations) / len(durations)

    # returns the average and the len of the movies
    return result, len(durations)
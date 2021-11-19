import requests, json, os

storge_db = f"{os.environ['STORGE_FULL_PATH']}/storage.json"

def obj_from_finout():
    '''

    '''
    # get the obj from finout app
    res = requests.get(os.environ['FINOUT_SERVER_URL'])

    # retry request in case of error
    if res.status_code >= 500:
        return obj_from_finout()

    # returns the test on str
    return res.text

class Object:
    '''
    read / write class function
    '''
    def read():

        file = open(storge_db, "r")
        return json.load(file)

    def write():
        return open(storge_db, "w")

def update_movie_storage(data):
    '''
    check if the movie dosn't exist and
    update the storage
    '''
    # use with finout api app
    data = json.loads(data)
    # check if the file exist or empty
    movie_info = { "name": data["title"], "duration": data["duration"] }
    if not os.path.exists(storge_db) or os.stat(storge_db).st_size == 0:
        empty_storage = Object.write()
        obj = { "movies": [ movie_info ] }
        empty_storage.write(json.dumps(obj))
        empty_storage.close

    else:
        movie_list = []
        existing_storage = Object.read()

        # add the movie to the movie array
        for movie in existing_storage["movies"]:
            movie_list.append(movie["name"])

        # check if there isn't a duplicates between the new data and the existing data
        if data["title"] not in movie_list:
            existing_storage["movies"].append(movie_info)
            content = Object.write()
            content.write(json.dumps(existing_storage))
            content.close

def last_ten_movies():
    '''
    returns the last 10 movies
    '''
    last_movies = []
    number = 0
    # check if the file exist or empty
    if not os.path.exists(storge_db) or os.stat(storge_db).st_size == 0:
        return None

    movies = Object.read()
    # get the last 10 movies
    movies_obj = movies.get("movies")[-10:]

    # add the last 10 movies to an array
    for movie in movies_obj:
        number += 1
        last_movies.append({ f"Movie number {number}": movie["name"]})
    return last_movies

# Get the average of all movies that the user has watched
```
curl localhost:5001/api/v1/average -w %{http_code}
```
# Get the 10 last movies that the user has watched
```
curl localhost:5001/api/v1/last_movies -w %{http_code}
```
# Get the object after filtered
```
curl localhost:5001/api/v1/movie -w %{http_code}
```
```
Local app: set correctly the environment variables in ".env" file.
Docker app: set correctly the environment variables in "docker-compose.yaml" file.
```
There is a makefile as an extra :D

# TODO:
Create a simple MongoDB server.

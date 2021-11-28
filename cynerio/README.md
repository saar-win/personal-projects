### Writing to redis application

# The goal of this exercise is to build a small web service with db.

- There is a few endpoints for the app
- Redis as db


# Healthcheck
```
curl http://${IP}/healthcheck
```

# Writing to redis DB, using:
```
    curl \
        --request POST \
        --data '{"id": "zero", "data": "one"}' \
        http://localhost:5000/set
```

# Get data from DB by the id, using:
```
    id=one
        curl http://localhost:5000/get/{id}
```
# Delete data from DB by the id, using:
```
    id=one
        curl http://localhost:5000/delete/{id}
```
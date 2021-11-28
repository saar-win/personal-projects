### A simple app for writing object to redis
#
- In this project, I'm using "kind" as a cluster.
- A helper Makefile for easy control.
- There is a cron job that runs once an hour.
- The cronjob sending a curl request that writes to Redis the object that gets from the StarWars API
- K8S included StatefulSet as a deployment to avoid loss of information.
# To run locally, using:
```
make docker-redis-run
make docker-immunai-run
```
# To run on k8s(kind), using:
```
make helm-apply
```
# To delete from k8s(kind), using:
```
make helm-delete
```
# To interact with the app, using:
```
curl localhost:5000/api/v1/write
curl localhost:5000/api/v1/read
```
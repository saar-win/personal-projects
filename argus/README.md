# This Sample-app deployment by customizing helm chart.
# Included files:
#
k8s:
    - values.yaml
    - charts
    - templates:
        - service.yaml
        - deployment.yaml

- The "values.YAML" holds the environment variables values to keep the template generic as much as possible.
- In addition, there is a simple UI that shows the user the times in cities around the world.
- There is a Makefile for running the commands.

- To use with Helm just run:
```
make build-deploy
```

- To locally use, just run:
```
make docker-build
```

"GET" request:
```
curl http//IP:80/
```
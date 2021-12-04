# Create a deployment process on a EKS cluster

- Github actions create the process, triggered by pr.
- A helper Makefile for easy control.
### macOS deps:
```
brew install awscli
```

### To build the image, using:
```
make docker-build
```
### To push the image to dockerhub, using:
```
make docker push
```
### To connect to the cluster, using:
```
aws sts get-caller-identity
aws eks --region region update-kubeconfig --name cluster_name
```
#
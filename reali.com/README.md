# Create a deployment process on a EKS cluster

- Github actions create the process, triggered by pr.
- A helper Makefile for easy control.
### macOS deps:
```
brew install awscli \
brew install weaveworks/tap/eksctl
```
### On the cluster have to install a loadBalancer:
```
https://kubernetes.github.io/ingress-nginx/deploy/
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

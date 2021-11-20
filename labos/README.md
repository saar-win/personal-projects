### Hello World app
# included files:
```
    - ansible/
        - rols/
        - vars/
        ...
    - terraform/
        - gke-cluster
        - kubernetes-config
        ...
    - customer/
        - api/
            - v1/
                - main.py
    - k8s/
        ...
    - docker-compose.yaml
    - Dockerfile
    - Makefile
```
- Create a k8s cluster by terraform script.
- Deploy the K8S ingress by ansible.
- Deploy the application by ansible.
- The goal of this project is build the cluster with
    one technology and deploy the application with the other technology.
# To locally use (just the app), run:
```
make run-local
```
# To deploy a new K8S cluster, run:
```
terraform plan
terraform apply
```
# To deploy the application by ansible on a K8S environment, run:
```
make build-deploy-all
```
# To destroy the K8S cluster, run:
```
terraform destroy
```
# To destroy the application by ansible on a K8S environment, run:
```
make destroy-all
```
# To interact with the page
```
curl http://$IP:80/customer/v1 -w %{http_code}
```

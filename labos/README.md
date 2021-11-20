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
- Create a k8s cluster using terraform script.
- Deploy the K8S ingress using ansible.
- Deploy the application using ansible.
- The goal of this project is to build the cluster with
    one technology and deploy the application with the other technology.
# To run application locally, run:
```
make run-local
```
# To deploy a new K8S cluster, run:
```
terraform plan
terraform apply
```
# To deploy the application using ansible on a K8S environment, run:
```
make build-deploy-all
```
# To destroy the K8S cluster, run:
```
terraform destroy
```
# To destroy the application using ansible on a K8S environment, run:
```
make destroy-all
```
# To interact with the page
```
curl http://$IP:80/customer/v1 -w %{http_code}
```

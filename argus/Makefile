docker-push:
	docker tag sample:latest wintrov/sample:latest
	docker push wintrov/sample:latest

docker-build:
	docker build . -t sample:latest -f ./Dockerfile

helm-apply:
	helm template k8s --name sample --namespace test | kubectl apply -f-

helm-delete:
	helm template k8s --name sample --namespace test | kubectl delete -f-

get-ip:
	kubectl get ingress basic-ingress | awk '{print $$4}' | awk 'NR == 2'

build-deploy:
	make docker-build
	make docker-push
	make helm-apply
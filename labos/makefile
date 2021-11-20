get-hello:
	curl http://localhost:5000/customer/v1 -w %{http_code}

docker-build-run:
	docker-compose up -d --build labos

docker-build:
	docker-compose build labos

run-local:
	flask run

docker-push:
	docker tag labos:latest wintrov/labos:latest
	docker push wintrov/labos:latest

deploy-app:
	ansible-playbook ansible/application.yaml --extra-vars "state=present"

destroy-app:
	ansible-playbook ansible/application.yaml --extra-vars "state=absent"

deploy-ingress:
	ansible-playbook ansible/ingress.yaml --extra-vars "state=present"

destroy-ingress:
	ansible-playbook ansible/ingress.yaml --extra-vars "state=absent"

build-deploy-all:
	make docker-build
	make docker-push
	make deploy-ingress
	make deploy-app

destroy-all:
	make destroy-app
	make destroy-ingress

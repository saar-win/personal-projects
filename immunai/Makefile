docker-redis-run:
	docker-compose up -d redis_json

docker-immunai-run:
	docker-compose up -d --build immunai

docker-build-push:
	docker-compose build immunai
	docker tag immunai wintrov/immunai:latest
	docker push wintrov/immunai:latest

helm-apply:
	helm template kind | kubectl apply -f-

helm-delete:
	helm template kind | kubectl delete -f-

port-forward:
	kubectl port-forward --address localhost,0.0.0.0 service/immunai 5000:5000
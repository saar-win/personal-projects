get-hello:
	curl http://localhost:5000/customer/v1 -w %{http_code}

docker-build-run:
	docker-compose up -d --build labos

run-local:
	flask run
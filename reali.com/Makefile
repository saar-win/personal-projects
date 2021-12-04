docker-build:
	docker build ./app -f ./app/Dockerfile -t reali:latest

docker-push:
	docker tag reali:latest wintrov/reali:latest
	docker push wintrov/reali:latest
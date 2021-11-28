docker-build-cynerio:
	docker-compose build cynerio

docker-run-cynerio:
	docker-compose up -d cynerio

docker-run-redis:
	docker-compose up -d redis

docker-run-all:
	make docker-run-redis
	make docker-run-cynerio
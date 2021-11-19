build-math:
	docker-compose build math

run-math:
	docker-compose up -d math

build-audit:
	docker-compose build audit

run-audit:
	docker-compose up -d audit

run-mongodb:
	docker-compose up -d mongodb

build-nginx:
	docker-compose build nginx

run-nginx:
	docker-compose up -d nginx

build-run-all:
	docker-compose up -d --build nginx
	docker-compose up -d --build math
	docker-compose up -d --build audit
	docker-compose up -d --build mongodb
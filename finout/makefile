docker-build-run:
	docker-compose up -d --build saar_app

docker-down:
	docker-compose down

get_average:
	curl localhost:5001/api/v1/average -w %{http_code}

get_last_movies:
	curl localhost:5001/api/v1/last_movies -w %{http_code}

get_movie:
	curl localhost:5001/api/v1/movie -w %{http_code}
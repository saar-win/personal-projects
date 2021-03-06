#! /bin/bash
cat << EOF > ~/docker-compose.yaml
version: '3.6'
services:
#############################################
  flask-helloworld:
    container_name: flask-helloworld
    image: digitalocean/flask-helloworld:latest
    restart: always
    networks:
        - saar-network
    ports:
        - 5000:5000
    expose:
        - 5000
#############################################
  postgres_db:
    container_name: postgres_db
    image: redislabs/rejson:latest
    restart: always
    ports:
        - 5432:5432
    networks:
        - saar-network
    volumes:
        - ./objects:/app/objects
#############################################
  nginx:
    container_name: nginx
    image: wintrov/nginx:latest
    restart: always
    ports:
        - 80:80
    networks:
        - saar-network
#############################################
networks:
    saar-network:
EOF

sudo docker-compose up -d flask-helloworld
sudo docker-compose up -d --build nginx
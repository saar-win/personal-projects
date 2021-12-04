#!/bin/bash
mkdir /home/scripts
cat << EOF > /home/scripts/docker-compose.yaml
version: '3.6'
services:
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
  nginx:
    container_name: nginx
    image: wintrov/nginx:latest
    restart: always
    ports:
        - 80:80
    networks:
        - saar-network
networks:
    saar-network:
EOF
echo "Docker compose file has been written"

## install docker:
sudo apt-get update

sudo apt-get install ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io -y

## install docker-compose:
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

cd /home/scripts && sudo docker-compose up -d flask-helloworld nginx

dir="/mnt/db"
if [[ ! -d "$dir" ]]; then
    echo "Trying to create a connection to persistent disk"
    sudo mkdir /mnt/db
    sudo mount -o discard,defaults /dev/sdb /mnt/db
fi
sleep 1
cmd=$(lsblk | grep sdb | awk '{print $7}')
if [[ -z "$cmd"  ]]; then
    echo "Trying to associate persistent disk"
    sudo mkdir /mnt/db
    sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb
    sudo mount -o discard,defaults /dev/sdb /mnt/db
fi
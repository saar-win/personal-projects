# init the base image
FROM ubuntu:20.04

# set workdir
WORKDIR /app

# no gui step
ARG DEBIAN_FRONTEND=noninteractive

# update the system operation
RUN apt-get update

# install deps
RUN apt install -y \
    software-properties-common \
    sudo \
    curl \
    npm \
    python3.9 \
    python3-pip
# add repo
RUN add-apt-repository ppa:deadsnakes/ppa

# copy file
COPY ./api/v1 ./api/v1

# install the req
RUN pip install -r ./api/v1/requirements.txt

# add user step
RUN adduser --disabled-password --gecos '' test
RUN echo 'test ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# set the endpoint user
USER test

# run the app
CMD [ "flask", "run", "--host=0.0.0.0" ]
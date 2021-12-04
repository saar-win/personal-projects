FROM ubuntu:latest
# set the workdir
WORKDIR /app
# non GUI
ARG DEBIAN_FRONTEND=noninteractive
# install ubuntu update
RUN apt-get update
# install the dependencies
RUN apt install -y \
    software-properties-common \
    sudo \
    curl \
    npm \
    python3.9 \
    python3-pip
#
RUN add-apt-repository ppa:deadsnakes/ppa
# install fs tools
RUN npm install -g node-firestore-import-export
# copy the req and the main files
COPY . .
# isntall the req
RUN pip install -r requirements.txt
# install the gCloud deps
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN sudo apt-get install apt-transport-https ca-certificates gnupg -y
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN sudo apt-get update && sudo apt-get install google-cloud-sdk -y
# set the Env flask Port
ARG FLASK_PORT
ENV FLASK_RUN_PORT=${FLASK_PORT}
# set the Env flask App
ARG FLASK_APP
ENV FLASK_APP=${FLASK_APP}
# Run the server
CMD ["flask", "run", "--host=0.0.0.0"]
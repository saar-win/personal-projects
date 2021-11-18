# init the base image
FROM python:3.8-alpine as base
#
WORKDIR /app

# copy file
COPY ./sample/api/v1 ./sample/api/v1

# copy the req file
COPY ../requirements.txt requirements.txt

# install the req
RUN pip install -r requirements.txt

# defines the env var
ENV FLASK_RUN_PORT=80
ENV FLASK_APP=sample/api/v1/main.py

# run the app
CMD [ "flask", "run", "--host=0.0.0.0" ]
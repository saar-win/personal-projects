# init the base image
FROM python:3.8.0-buster as base
#
WORKDIR /app

# copy utils
COPY ../package package

# copy file
COPY ./api/v1 ./api/v1

# install the req
RUN pip install -r ./api/v1/requirements.txt

# run the app
CMD ["flask", "run", "--host=0.0.0.0"]
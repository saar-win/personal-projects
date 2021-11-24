# init the base image
FROM python:3.8-alpine as base
#
WORKDIR /app

# copy file
COPY ./api/v1 ./api/v1

# install the req
RUN pip install -r ./requirements.txt

# run the app
CMD [ "flask", "run", "--host=0.0.0.0" ]
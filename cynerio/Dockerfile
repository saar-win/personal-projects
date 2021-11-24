# init the base image
FROM python:3.8.0-alpine
#
WORKDIR /app

# copy file
COPY ./api/v1 ./api/v1
COPY ./package package

# install the req
RUN pip install -r ./api/v1/requirements.txt

# run the app
CMD ["flask", "run", "--host=0.0.0.0"]
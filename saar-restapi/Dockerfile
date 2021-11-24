# init the base image
FROM python:3.8.0-buster as base
#
WORKDIR /app

# copy utils
COPY ../modules modules

# copy file
ARG APP
COPY ./${APP}/api/v1 ./${APP}/api/v1

# copy the req file
COPY ../requirements.txt requirements.txt

# install the req
RUN pip install -r requirements.txt

# run the app
CMD ["flask", "run", "--host=0.0.0.0"]
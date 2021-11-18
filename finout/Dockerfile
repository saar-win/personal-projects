# init the base image
FROM python:3.8.0-buster as base
#
WORKDIR /app

# copy utils
COPY ../package package


# copy file
ARG APP
COPY ./${APP}/api/v1/main.py ./${APP}/api/v1/main.py

# copy the req file
COPY ../requirements.txt requirements.txt

# install the req
RUN pip install -r requirements.txt

# defines the env var
ARG FLASK_RUN_PORT
ARG FLASK_APP
ENV FLASK_RUN_PORT=${FLASK_RUN_PORT}
ENV FLASK_APP=${FLASK_APP}

# set the python path
ENV PYTHONPATH="${PYTHONPATH}:/app/package"

# run the app
CMD ["flask", "run", "--host=0.0.0.0"]
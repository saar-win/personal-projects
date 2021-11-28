# init the base image
FROM python:3.8.0-alpine as base

# set workdir
WORKDIR /app

# copy file
COPY . .

# install the req
RUN pip install -r ./api/v1/requirements.txt

# set python path
ENV PYTHONPATH="${PYTHONPATH}:/app/package"

# create a cron job
CMD [ "flask" , "run" , "--host=0.0.0.0" ]
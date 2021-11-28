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
RUN ln -sf /proc/1/fd/1 /var/log/app.log
RUN echo '* * * * * curl localhost:5000/api/v1/write > /var/log/app.log' > /etc/crontabs/root

# run the app
RUN chmod +x ./scripts/*
CMD [ "./scripts/entrypoint.sh" ]
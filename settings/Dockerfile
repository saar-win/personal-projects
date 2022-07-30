# base img
FROM node:14.19.3

# defines workdir
WORKDIR /app

# copy the main file
COPY setup.sh /app/setup.sh

# run the main file
ENTRYPOINT ["/app/setup.sh"]
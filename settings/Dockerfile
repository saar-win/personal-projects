# base img
FROM bash:4.4

# defines workdir
WORKDIR /app

# copy the main file
COPY setup.sh /app/setup.sh

# run the main file
ENTRYPOINT ["/app/setup.sh"]
# base img
FROM alpine:latest

LABEL "com.github.actions.name"="git-settings"
LABEL "com.github.actions.description"="A settings before run actions"
LABEL "com.github.actions.icon"="hash"
LABEL "com.github.actions.color"="black"

RUN set -e -x; \
        apk add --no-cache \
            bash \
            curl \
            jq \
            git \
            coreutils \
            openssh-client

# defines workdir
WORKDIR /app

# copy the main file
COPY setup.sh /app/setup.sh

# run the main file
ENTRYPOINT ["/app/setup.sh"]
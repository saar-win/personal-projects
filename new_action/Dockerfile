# base img
FROM python:3.10

# defines workdir
WORKDIR /app

# copy the main file
COPY main.py /app/main.py

COPY setup_git.sh /app/setup_git.sh

# copy templates file
COPY templates/ ./templates/

# compy the req file
COPY requirements.txt requirements.txt

# install req
RUN pip install -r ./requirements.txt

ENV USER_NAME USER_NAME
ENV PASSWORD PASSWORD

RUN git config --global --add url."https://$USER_NAME:$PASSWORD@github.com/".insteadOf "https://github.com/"

# run the main file
ENTRYPOINT ["python3", "/app/main.py"]
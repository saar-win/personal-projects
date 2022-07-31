# base img
FROM python:3.10

# defines workdir
WORKDIR /app

# copy the main file
COPY main.py /app/main.py

# copy templates file
COPY templates ./templates

# compy the req file
COPY requirements.txt requirements.txt

# install req
RUN pip install -r ./requirements.txt

# # add user step
# RUN adduser --disabled-password --gecos '' rapidapi
# RUN echo 'rapidapi ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# # define the user
# USER rapidapi

# run the main file
ENTRYPOINT ["python3", "/app/main.py"]
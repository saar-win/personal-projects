# set the image
FROM python:3.8 as base

# set the workdir
WORKDIR /app

# copy files
ADD . .

# install the reqs
RUN pip install -r requirements.txt

# port env
EXPOSE 5000

# run the app
CMD ["python", "app/main.py"]
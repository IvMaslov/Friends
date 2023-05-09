
FROM python:3.8
ENV DockerHOME=/home/app/friends
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

RUN pip install --upgrade pip

COPY . $DockerHOME
RUN pip install -r requirements.txt

EXPOSE 8000  
RUN python3 manage.py runserver


# docker build . -t friends-to-docker --network=host --rm
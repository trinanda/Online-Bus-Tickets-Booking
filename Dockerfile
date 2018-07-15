FROM python:3.6.5-stretch

MAINTAINER Nadia Azizah

RUN apt-get update && apt-get install -y build-essential libpq-dev

ENV INSTALL_PATH_DI_DALAM_DOCKER /web_app_docker

RUN mkdir -p $INSTALL_PATH_DI_DALAM_DOCKER

WORKDIR $INSTALL_PATH_DI_DALAM_DOCKER

COPY requirements.txt requirements_docker.txt

RUN pip install -r requirements_docker.txt

COPY . .

CMD gunicorn -b 0.0.0.0:80 --access-logfile - "web_app.app:create_app()"

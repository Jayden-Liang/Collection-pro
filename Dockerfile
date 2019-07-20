FROM python:3.6-slim
MAINTAINER Nick Janetakis <nick.janetakis@gmail.com>


RUN apt-get update && apt-get install -y gcc
RUN apt-get update && apt-get -y install default-libmysqlclient-dev
RUN apt-get install MariaDB-devel MariaDB-shared

ENV INSTALL_PATH /project
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt

RUN pip3 install mysqlclient==1.3.6
RUN pip3 install -r requirements.txt


COPY . .
RUN pip3 install --editable .

CMD gunicorn -c "python:config.gunicorn" "project.app:create_app()"

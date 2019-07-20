FROM python:3.7


RUN apt-get update && apt-get install -y gcc
RUN apt-get update && apt-get -y install python3-dev
RUN apt-get update && apt-get -y install default-libmysqlclient-dev



ENV INSTALL_PATH /project
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt

RUN pip3 install mysqlclient
RUN pip3 install -r requirements.txt


COPY . .
RUN pip3 install --editable .

CMD gunicorn -c "python:config.gunicorn" "project.app:create_app()"

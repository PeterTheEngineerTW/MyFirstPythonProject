# Base img
FROM ubuntu:18.04

## Python
# Install python 3.7
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.7 python3.7-dev python3-pip
# Create soft link for python 3.7
RUN ln -sfn /usr/bin/python3.7 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python && ln -sfn /usr/bin/pip3 /usr/bin/pip

WORKDIR /app
ADD . /app

## Install curl for health check
RUN apt-get install -y curl

## Install sql client
RUN apt-get install -y libmysqlclient-dev

## Install requirements
RUN pip install -r requirements.txt

## Install uwsgi plugin
#RUN apt-get install -y uwsgi-plugins-all
RUN apt-get update && apt-get install -y uwsgi-plugin-python3

EXPOSE 8080

ADD ./startup.sh /app
RUN chmod +x '/app/startup.sh'
RUN chmod +x '/app/wait-for-it.sh'
CMD /app/startup.sh
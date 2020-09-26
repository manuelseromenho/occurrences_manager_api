FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y && apt-get upgrade --fix-missing -y
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    python-pip \
    python-dev \
    libpq-dev \
    gettext \
    libreadline-dev \
    libssl-dev \
    libjpeg-dev \
    libfreetype6-dev \
    binutils \
    libproj-dev \
    gdal-bin \
    postgis


RUN pip install --upgrade pip

RUN mkdir /code
ADD . /code/

WORKDIR /code/
RUN pip install -r requirements/base.pip

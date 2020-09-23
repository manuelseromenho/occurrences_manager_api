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
    postgis \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# It won't run from the root user.
RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

RUN pip install --upgrade pip

RUN mkdir /code
ADD . /code/

WORKDIR /code/
RUN pip install -r requirements/local.pip

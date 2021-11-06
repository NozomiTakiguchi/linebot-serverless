FROM python:3.7.3-slim
USER root
# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

WORKDIR /opt/python/bin
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    apt-utils \
    gcc \
    build-essential \
    && apt-get install -y wget \
    && apt-get install -y unzip \
    && apt-get install -y vim less curl\
    && apt-get install -y vim lsof\
    && apt-get install -y gnupg
RUN apt update \
  && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt-get install -y ./google-chrome-stable_current_amd64.deb \
  && apt clean \
  && rm -rf /var/lib/apt/lists/ \
  && rm google-chrome-stable_current_amd64.deb

RUN pip install selenium chromedriver-binary~=$(/usr/bin/google-chrome --version | perl -pe 's/([^0-9]+)([0-9]+\.[0-9]+).+/$2/g')
RUN pip install --upgrade pip

WORKDIR /opt/app
COPY requirements.lock /opt/app
RUN pip install -r requirements.lock

ENTRYPOINT ["/bin/sh", "-c", "while :; do sleep 10; done"]
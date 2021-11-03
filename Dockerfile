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

# setup for web-scraping
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && apt install -y ./google-chrome-stable_current_amd64.deb \
#     && rm ./google-chrome-stable_current_amd64.deb \
#     && curl -fsSL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip > headless-chronium.zip \
#     && unzip -o headless-chronium.zip -d . \
#     && rm headless-chronium.zip \
# RUN wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip \
#     && unzip chromedriver_linux64.zip \
#     && rm ./chromedriver_linux64.zip \
#     && wget https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip \
#     && unzip IPAexfont00401.zip -d ~/.fonts/ \
#     && apt-get autoremove -y \
#     && apt-get clean -y \
#     && rm -rf /var/lib/apt/lists/*

# setup for auzre functions
# WORKDIR /opt/keys
# RUN apt-get update \
#     # apt-transport-https がないと The method driver /usr/lib/apt/methods/https could not be found. と怒られる
#     && apt-get install -y lsb-release gnupg2 apt-transport-https curl
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
#     && mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg \
#     && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/debian/$(lsb_release -rs | cut -d'.' -f 1)/prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list' \
#     && apt-get update \
#     && apt-get install azure-functions-core-tools-3

RUN pip install --upgrade pip

WORKDIR /opt/app
COPY requirements.lock /opt/app
RUN pip install -r requirements.lock

ENTRYPOINT ["/bin/sh", "-c", "while :; do sleep 10; done"]
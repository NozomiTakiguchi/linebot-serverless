FROM python:3.7.3-slim

ARG USERNAME=vscode
ARG UID=1000
ARG GID=$UID

ARG SAMCLI_FILE=aws-sam-cli-linux-x86_64
ARG DEFAULT_SAMCLI_VERSION=v1.33.0
# https://github.com/aws/aws-sam-cli/releases/latest から取得 (作成時 latest = v1.33.0)
ARG DEFAULT_SAMCLI_SHA256=3fcdf752ab30e6355087bcfa451a7d3ca6eb23445b893ecfcd0dea4fab166382

RUN groupadd --gid ${GID} ${USERNAME} \
    # ホームディレクトリ作成, ログインシェルを /bin/sh -> /bin/bash に変更
    && useradd --uid ${UID} --gid ${GID} -m ${USERNAME} -s /bin/bash \
    && apt-get update \
    && apt-get install -y sudo procps coreutils curl unzip docker \
    && echo 'alias ll="ls -sl"' >> /home/${USERNAME}/.bashrc \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}

WORKDIR /tmp
# https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html に従う
RUN /bin/bash -c "curl -fsSOL https://github.com/aws/aws-sam-cli/releases/download/v1.33.0/${SAMCLI_FILE}.zip" \
    # sha256 が間違っている場合は "sha256sum: 'standard input': no properly formatted SHA256 checksum lines found" と怒られる
    && echo "${DEFAULT_SAMCLI_SHA256} /tmp/${SAMCLI_FILE}.zip" | sha256sum -c \
    && sudo unzip aws-sam-cli-linux-x86_64.zip -d sam-installation \
    && sudo ./sam-installation/install

RUN /bin/bash -c "curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"" \
    && unzip awscliv2.zip \
    && sudo ./aws/install

WORKDIR /home/${USERNAME}
# https://docs.docker.com/engine/install/debian/ に従う
RUN sudo apt-get update \
    && sudo apt-get install -y apt-transport-https ca-certificates gnupg lsb-release
RUN /bin/bash -c "curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg"
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN sudo apt-get update \
    && sudo apt-get install -y docker-ce docker-ce-cli containerd.io


USER root
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
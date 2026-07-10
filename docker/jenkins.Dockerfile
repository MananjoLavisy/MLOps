FROM docker:cli AS docker-cli

FROM jenkins/jenkins:lts

USER root

RUN git config --system --add safe.directory '*'

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

USER jenkins

FROM docker:cli AS docker-cli

FROM jenkins/jenkins:lts

USER root

RUN git config --system --add safe.directory '*'

COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

USER jenkins

FROM alpine:3.18.0
LABEL repo=https://github.com/arsiac/temurin-image
WORKDIR /
ARG Package
ARG FolderName
ENV JAVA_HOME=/opt/${FolderName}
COPY ${Package} /opt/${FolderName}
RUN ln -s ${JAVA_HOME}/bin/java /usr/bin/java

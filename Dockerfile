FROM alpine
WORKDIR /
ARG Package
ARG FolderName
ENV JAVA_HOME=/opt/${FolderName}
COPY ${Package} /opt/${FolderName}
RUN ln -s ${JAVA_HOME}/bin/java /usr/bin/java

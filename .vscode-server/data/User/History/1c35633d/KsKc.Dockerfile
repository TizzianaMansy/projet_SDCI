FROM node:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils

#CMD /bin/bash

#our code starts here
WORKDIR /app
RUN npm install express
RUN npm install systeminformation
COPY . /app/server.js
EXPOSE 8080


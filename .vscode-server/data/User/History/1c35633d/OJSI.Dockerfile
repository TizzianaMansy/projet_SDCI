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
RUN npm install
RUN npm install express
RUN npm install systeminformation
COPY . /app/server.js
EXPOSE 8080
CMD ["node", "server.js", "--local_ip", "127.0.0.1", "--local_port", "8080", "--local_name", "srv"]

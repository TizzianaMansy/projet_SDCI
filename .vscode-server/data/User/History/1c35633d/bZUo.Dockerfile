FROM node:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils



#our code starts here
WORKDIR /app
RUN curl -o server.js https://homepages.laas.fr/smedjiah/tmp/mw/server.js
RUN npm install express systeminformation yargs request

COPY . /app/server.js
EXPOSE 8080

CMD /bin/bash

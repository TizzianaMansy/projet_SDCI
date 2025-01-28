FROM node:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils \
        curl



#our code starts here
WORKDIR /app
RUN curl -o server.js https://homepages.laas.fr/smedjiah/tmp/mw/server.js
RUN curl -o application.js https://homepages.laas.fr/smedjiah/tmp/mw/application.js
RUN npm install express systeminformation yargs request

EXPOSE 8080

CMD /bin/bash

FROM node:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils \
        curl


WORKDIR /app
RUN curl -o gateway.js https://homepages.laas.fr/smedjiah/tmp/mw/gateway.js
RUN npm install express systeminformation yargs request

CMD /bin/bash
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
RUN curl -o gateway.js https://homepages.laas.fr/smedjiah/tmp/mw/gateway.js
RUN curl -o device.js https://homepages.laas.fr/smedjiah/tmp/mw/device.js 
RUN npm install express systeminformation yargs request

COPY start_gf_device.sh /app/start_gf_device.sh

CMD /bin/bash

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
RUN curl -o server.js https://homepages.laas.fr/smedjiah/tmp/mw/server.js
RUN curl -o gateway.js https://homepages.laas.fr/smedjiah/tmp/mw/gateway.js
RUN curl -o application.js https://homepages.laas.fr/smedjiah/tmp/mw/application.js
RUN curl -o device.js https://homepages.laas.fr/smedjiah/tmp/mw/device.js
RUN npm install express systeminformation yargs request

CMD /bin/bash
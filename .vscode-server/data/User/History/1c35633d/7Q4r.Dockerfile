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
COPY /home/sdci/.vscode-server/cli/servers/Stable-fabdb6a30b49f79a7aba0f2ad9df9b399473380f/server/node_modules/opentype.js/bin/server.js /app/server.js
EXPOSE 8080
CMD ["node", "server.js", "--local_ip", "127.0.0.1", "--local_port", "8080", "--local_name", "srv"]

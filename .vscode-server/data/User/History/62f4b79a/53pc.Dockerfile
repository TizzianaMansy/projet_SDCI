FROM python:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils

WORKDIR /app

COPY monitor.py /app/monitor.py
RUN npm install requests time logging

CMD /bin/bash

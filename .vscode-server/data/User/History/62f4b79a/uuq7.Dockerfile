FROM python:alpine

RUN apk add --update --no-cache \
                bash \
                tcpdump \
                iperf \
                busybox-extras \
                iproute2 \
                iputils \
                curl

WORKDIR /app

COPY monitor.py /app/monitor.py
RUN pip install --no-cache-dir requests

CMD /bin/bash

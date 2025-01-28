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

COPY ryu.py /app/ryu.py
RUN pip install ryu requests
CMD /bin/bash

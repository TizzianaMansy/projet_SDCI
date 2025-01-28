FROM python:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils \
	net-tools

EXPOSE 5000
ENV VIM_EMU_CMD "echo 'Starting the container...'"
ENV VIM_EMU_CMD_STOP "echo 'Stopping the container...'"

CMD /bin/bash

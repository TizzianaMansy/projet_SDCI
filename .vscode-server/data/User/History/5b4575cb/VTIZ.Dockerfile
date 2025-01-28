FROM python:alpine

RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils \
	net-tools
        
WORKDIR /app

COPY monitor.py /app/monitor.py
RUN pip install --no-cache-dir requests
        
ENV VIM_EMU_CMD "python3 /app/monitor.py"
ENV VIM_EMU_CMD_STOP "echo 'Stopping the container...'"

CMD /bin/bash

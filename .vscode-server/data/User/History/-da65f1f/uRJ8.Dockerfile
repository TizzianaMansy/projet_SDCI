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

COPY ordonnanceur.py /app/ordonnanceur.py
RUN pip install --no-cache-dir requests flask scapy jsonify
   
ENV VIM_EMU_CMD "python3 /app/ordonnanceur.py"
ENV VIM_EMU_CMD_STOP "echo 'Stopping the container...'"

CMD /bin/bash

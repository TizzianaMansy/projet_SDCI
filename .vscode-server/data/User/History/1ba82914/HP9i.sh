#!/bin/bash


# Start gateway.js
node gateway.js --local_ip "0.0.0.0" --local_port 8080 --local_name ${LOCALNAMEGW} --remote_ip ${REMOTEIP} --remote_port 8080 --remote_name ${REMOTENAMEGW} &

# Start device.js
node device.js --local_ip "0.0.0.0" --local_port 8080 --local_name ${LOCALNAMEDEV} --remote_ip "127.0.0.1" --remote_port 8080 --remote_name ${LOCALNAMEGW} --send_period ${PERIOD} &


/bin/bash

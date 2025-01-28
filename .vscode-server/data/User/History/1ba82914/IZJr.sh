#!/bin/bash


# Start gateway.js
node gateway.js --local_ip "127.0.0.1" --local_port 8282 --local_name ${LOCALNAMEGW} --remote_ip ${REMOTEIP} --remote_port 8181 --remote_name ${REMOTENAMEGW} &

# Start device.js
node device.js --local_ip "127.0.0.1" --local_port 9001 --local_name ${LOCALNAMEDEV} --remote_ip "127.0.0.1" --remote_port 8282 --remote_name ${REMOTENAMEDEV} --send_period ${PERIOD} &


/bin/bash

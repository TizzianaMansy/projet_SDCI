#!/bin/bash

# Start gateway.js
node gateway.js --local_ip "0.0.0.0" --local_port 8080 --local_name ${LOCALNAME} --remote_ip ${REMOTEIP} --remote_port 8080 --remote_name ${REMOTENAME}

/bin/bash
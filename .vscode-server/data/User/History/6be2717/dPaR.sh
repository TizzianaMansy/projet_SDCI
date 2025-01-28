#!/bin/bash


# Start gateway.js
node gateway.js --local_ip "127.0.0.1" --local_port 8282 --local_name $NAME --remote_ip "127.0.0.1" --remote_port 8181 --remote_name "gwi"
 &


# Start device.js
node device.js --local_ip "127.0.0.1" --local_port 9001 --local_name "dev1" --remote_ip "127.0.0.1" --remote_port 8282 --remote_name "gwf1" --send_period 3000 &


/bin/bash


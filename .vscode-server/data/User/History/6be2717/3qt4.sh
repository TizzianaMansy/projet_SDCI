#!/bin/bash

# Start server.js
node server.js --local_ip "0.0.0.0" --local_port 8080 --local_name "srv" &

# Start application.js
node application.js --remote_ip "0.0.0.0" --remote_port 8080 --device_name "app1" --send_period 5000 &

/bin/bash
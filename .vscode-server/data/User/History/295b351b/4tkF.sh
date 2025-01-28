#!/bin/bash

# Start server.js
node server.js --local_ip "0.0.0.0" --local_port 8080 --local_name "srv" &

# Start application.js
node application.js --remote_ip "127.0.0.1" --remote_port 8080 --device_name "dev1" --send_period 5000 &

/bin/bash
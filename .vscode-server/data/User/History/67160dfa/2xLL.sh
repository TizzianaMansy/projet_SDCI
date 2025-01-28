#!/bin/bash

# Start node server.js
node /path/to/your/server.js --local_ip "127.0.0.1" --local_port 8080 --local_name "srv" &

# Start node application.js
node /path/to/your/application.js --remote_ip "127.0.0.1" --remote_port 8080 --device_name "dev1" --send_period 5000 &

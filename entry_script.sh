#!/bin/bash

# Start xvfb
/etc/init.d/xvfb start

# Set permissions for X11 Unix socket
chmod 1777 /tmp/.X11-unix

# Start Xvfb
# Xvfb :99 -screen 0 1280x720x24 &

# Wait for Xvfb to start
# sleep 5

# Run your Python script
python3 run.py

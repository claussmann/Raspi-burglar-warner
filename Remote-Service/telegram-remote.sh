#!/bin/bash
cd /etc/burglar_warner/remote
sleep 5
echo "Starting telegram remote service"
python2.7 service.py

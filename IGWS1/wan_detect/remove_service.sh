#!/bin/bash
sudo systemctl stop wan_detect.service
sudo systemctl disable wan_detect.service
sudo rm /etc/systemd/system/wan_detect.service
sudo systemctl daemon-reload
exec bash
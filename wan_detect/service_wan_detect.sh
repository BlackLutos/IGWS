#!/bin/bash
sudo cp ./wan_detect.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable wan_detect.service
sudo systemctl start wan_detect.service
sudo systemctl status wan_detect.service
exec bash
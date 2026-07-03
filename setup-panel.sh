#!/bin/bash
if [ ! -f /usr/sbin/pufferpanel ]; then
    curl -s https://packagecloud.io | sudo bash
    sudo apt-get update && sudo apt-get install pufferpanel -y
    sudo pufferpanel user add --name admin --email admin@example.com --password password123 --admin
fi
sudo /usr/sbin/pufferpanel start

#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

CURRENT_DIR=`pwd`

cd "$(dirname "$0")"

apt-get install -y supervisor

mkdir /home/pi/fan
mkdir /var/log/fan

cp ./fan.py /home/pi/fan/fan.py
cp ./fan.conf /etc/supervisor/conf.d/fan.conf

chown -R pi:pi /home/pi/fan
chown -R pi:pi /var/log/fan

supervisorctl reread
supervisorctl update

cd CURRENT_DIR

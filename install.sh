#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

CURRENT_DIR=`pwd`
USER=`id -nu 1000`

cd "$(dirname "$0")"

apt-get install -y supervisor

mkdir /home/$USER/fan
mkdir /var/log/fan

cp ./fan.py /home/$USER/fan/fan.py
cp ./fan.conf /etc/supervisor/conf.d/fan.conf

sed -i "s/{USER}/$USER/" /etc/supervisor/conf.d/fan.conf

chown -R $USER:$USER /home/$USER/fan
chown -R $USER:$USER /var/log/fan

supervisorctl reread
supervisorctl update

cd $CURRENT_DIR

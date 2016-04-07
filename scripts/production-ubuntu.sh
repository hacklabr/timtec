#!/bin/bash

TIMTEC_PRODUCTION_USER=vagrant

# production
sudo apt-get install -y nginx uwsgi
# Create uwsgi app
sudo cp timtec/scripts/conf/timtec-production.ini /etc/uwsgi/apps-available/
sudo ln -s /etc/uwsgi/apps-available/timtec-production.ini /etc/uwsgi/apps-enabled/timtec-production.ini

# configure nginx site
sudo cp timtec/scripts/conf/nginx-timtec-production /etc/nginx/sites-available/timtec-production
sudo ln -s /etc/nginx/sites-available/timtec-production /etc/nginx/sites-enabled/timtec-production
sudo nginx -s reload

# sudo useradd -U -m ${TIMTEC_PRODUCTION_USER}

# Database
# sudo su - postgres -c "createuser -d ${TIMTEC_PRODUCTION_USER}"

# sudo su - ${TIMTEC_PRODUCTION_USER}

# createdb ${TIMTEC_PRODUCTION_USER}

sudo su -l ${TIMTEC_PRODUCTION_USER} -c "bash -s" <<EOF
# git clone https://github.com/hacklabr/timtec.git
# cd timtec
# git checkout vagrant
# cd ..
# Don't forge to edit the file settings_production.py acording to your need. This is the file where you put your keys, passwords and secrets.
# cp -a timtec/timtec/settings_local_production.py settings_production.py
./timtec/scripts/env-setup.sh
cd timtec
make install
EOF

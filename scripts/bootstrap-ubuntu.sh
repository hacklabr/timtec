#!/bin/bash

TIMTEC_USER=vagrant

# useradd -U -m ${TIMTEC_USER}

## Install OS dependencies

sudo apt-get update
sudo apt-get install -y libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv nodejs npm git

# Ubuntu name the node binary nodejs
sudo ln -s /usr/bin/nodejs /usr/local/bin/node

## Database setup

sudo apt-get install -y postgresql
sudo su - postgres -c "createuser -d ${TIMTEC_USER}"
createdb timtec

./timtec/scripts/env-setup.sh

echo "source timtec-env/bin/activate" >> ~/.bashrc
echo "cd timtec" >> ~/.bashrc

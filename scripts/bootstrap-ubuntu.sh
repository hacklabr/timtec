#!/bin/bash

TIMTEC_USER=vagrant

## Install OS dependencies

# useradd --groups sudo --create-home ${TIMTEC_USER}

sudo apt-get update
sudo apt-get install -y libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv nodejs npm git

# sudo useradd -U -m ${TIMTEC_USER}

# Ubuntu name the node binary nodejs
sudo update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10

echo 'Installing database...'
## Database setup

sudo apt-get install -y postgresql
sudo su - postgres -c "createuser -d ${TIMTEC_USER}"
createdb ${TIMTEC_USER}

echo 'Done installing database!'

echo "source timtec-env/bin/activate" >> ~/.bashrc
echo "cd timtec" >> ~/.bashrc

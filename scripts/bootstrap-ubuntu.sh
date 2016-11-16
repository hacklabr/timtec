#!/bin/bash

TIMTEC_USER=vagrant
TIMTEC_VIRTUALENVFOLDER=~/env
TIMTEC_FOLDER=~/timtec

## Install OS dependencies

# useradd --groups sudo --create-home ${TIMTEC_USER}

sudo apt-get update
sudo apt-get install -y libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv git


curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get update
sudo apt-get install -y nodejs

# sudo useradd -U -m ${TIMTEC_USER}

# Ubuntu name the node binary nodejs
sudo update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10

echo 'Installing database...'
## Database setup

sudo apt-get install -y postgresql
sudo su - postgres -c "createuser -d ${TIMTEC_USER}"
createdb ${TIMTEC_USER}

echo 'Done installing database!'

## Create virtualenv

virtualenv ${TIMTEC_VIRTUALENVFOLDER}
source ${TIMTEC_VIRTUALENVFOLDER}/bin/activate

## Install depencencies and basic django setup

cd ${TIMTEC_FOLDER}

make


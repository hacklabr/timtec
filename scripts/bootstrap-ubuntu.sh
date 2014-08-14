#!/bin/bash

# TIMTEC_USER=timtec

# useradd -U -m ${TIMTEC_USER}

apt-get update
apt-get install -y libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv nodejs

# Database
# For timtec main project, we use postgresql to simulate prodution enviroment
# TODO: the developer version should use lighter databases, like sqlite.

# apt-get install -y postgresql

# production
# apt-get install -y nginx uwsgi

# su - ${TIMTEC_USER}
# virtualenv timtec-env
# source timtec-env/bin/activate
#cd timtec
# make

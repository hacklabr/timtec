#!/bin/bash

TIMTEC_VIRTUALENVFOLDER=~/env
TIMTEC_FOLDER=~/timtec

## Create virtualenv

virtualenv ${TIMTEC_VIRTUALENVFOLDER}
source ${TIMTEC_VIRTUALENVFOLDER}/bin/activate

## Install depencencies and basic django setup

cd ${TIMTEC_FOLDER}


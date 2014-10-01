# Timtec

[![Build Status](https://drone.io/github.com/hacklabr/timtec/status.png)](https://drone.io/github.com/hacklabr/timtec/latest)
[![Coverage](https://coveralls.io/repos/hacklabr/timtec/badge.png)](https://coveralls.io/r/hacklabr/timtec)


## Getting Started

We provide a vagrant file for easy dev environment creation. Install
[Vagrant](http://www.vagrantup.com/) and on the main directory run:

    vagrant up

See the Vagrantfile and script folder for more details.

## Dependencies


* Python 2.7 with virtualenv and pip
* build essentials and many dev packages if on apt/rpm based systems
    * libpq-dev, libjpeg-dev, libpng12-dev, build-essential, python-dev, gettext
* nodejs (0.10+) (you will need a ppa for ubuntu < 14.04)

### Python env


* create a Python 2.X virtualenv

    `virtualenv ../timtec-env`

* activate the virtual env

    `source ../timtec-env/bin/activate`

* run make

    `make`

* run the django devel server

    `./manage.py runserver`

## Running Tests

We made a bunch of tests for the system. They are separated into python tests
(that includes selenium full stack tests) and Karma/AngularJS tests. To run all
of them together just type

    make all_tests

remember that you need to have your virtualenv activated and has installed
everything from the `dev-requirements.txt` file.

### python

Activate virtual env, then:

    make python_tests

### Angular

In the root of repository:

    make karma_tests

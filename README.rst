Timtec
======

.. image:: https://drone.io/github.com/hacklabr/timtec/status.png
    :target: https://drone.io/github.com/hacklabr/timtec/latest

.. image:: https://coveralls.io/repos/hacklabr/timtec/badge.png
    :target: https://coveralls.io/r/hacklabr/timtec


Dependencies
------------

- Python 2.7 with virtualenv and pip
- build essentials and many dev packages if on debian/ubuntu/fedora
    - postgresql-client-dev, libjpeg-dev, libpng-dev, build-essential, python-dev
- nodejs (probably 0.8+ but tested on 0.10) (you will need a ppa for ubuntu < 14.04)

Getting Started
---------------

- create a Python 2.X virtualenv
- activate the virtual env
- go to this directory
- make
- ./manage.py runserver

Running Tests
-------------

run make all_tests to run all tests together

python
______

Activate virtual env, then:
make python_tests

Angular
_______

In the root of repository:

make karma_tests

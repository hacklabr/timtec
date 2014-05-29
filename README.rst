.. image:: https://badge.waffle.io/hacklabr/timtec.png?label=ready&title=Ready 
 :target: https://waffle.io/hacklabr/timtec
 :alt: 'Stories in Ready'
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
    - libpq-dev, libjpeg-dev, libpng12-dev, build-essential, python-dev, gettext
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

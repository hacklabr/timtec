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
- nodejs (probably 0.8+ but tested on 0.10)

Getting Started
---------------

- create a Python 2.X virtualenv
- activate the virtual env
- go to this directory
- pip install -r requirements.txt
- pip install -r dev-requirements.txt
- python setup.py develop
- sudo npm -g install less yuglify
- ./manage.py syncdb
- ./manage.py runserver

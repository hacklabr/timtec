Manual do Desenvolvedor
=======================


LICENSE - AGPLV3 
----------------


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see LICENSE file here or 
    `AGPLv3 <http://www.gnu.org/licenses>`_.


Deploy Requirements
-------------------

 * Operating system: Debian (>= 7.7) or Ubuntu (14.04);
 * Proxy server: uwsgi (>= 2.0.7);
 * Web Server: nginx (>= 1.6.2);
 * javascript server-side interpreter: node.js (>= 0.10.40);
 * Data base server: postgresql (>= 9.2);
 * Python language package: python (= 2.7 ou < 3);
 * Virtual Enviroment Python: virtualenv (>=1.11.6);

Develop Requirements
--------------------
 * all the above requirements
 * build essentials and many dev packages if on apt/rpm based systems
    * libpq-dev, libjpeg-dev, libpng12-dev, build-essential, python-dev, gettext
 * nodejs (0.10+) (you will need a ppa for ubuntu < 14.04)

Python env
----------

 * create a Python 2.X virtualenv::

    virtualenv ../timtec-env

 * activate the virtual env::

    source ../timtec-env/bin/activate

 * run make::

    make

 * run the django devel server::

    ./manage.py runserver

Getting Started
---------------

We provide a vagrant file for easy dev environment creation. Install
`Vagrant <http://www.vagrantup.com/>`_ and on the main directory run::

    vagrant up

Them you just need to go inside the machine to start the dev server::

    vagrant ssh

On the VM console::

    ./manage.py runserver 0.0.0.0:8000

Now the system is running, you can go to **http://localhost:8000** on your web
browser and navigate on it.

To create a new superuser (so you can give permissions to other make other users professors) run::

    ./manage.py createsuperuser

See the Vagrantfile and script folder for more details.

Running Tests
-------------

We made a bunch of tests for the system. They are separated into python tests
(that includes selenium full stack tests) and Karma/AngularJS tests. To run all
of them together just type::

    make all_tests

remember that you need to have your virtualenv activated and has installed
everything from the `dev-requirements.txt` file.

Python
------

Activate virtual env, then::

    make python_tests

Angular
-------

In the root of repository::

    make karma_tests


Source
------

 * `TIMTec Repo <https://github.com/institutotim/timtec>`_

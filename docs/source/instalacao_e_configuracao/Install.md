# About Tim Tec
Tim Tec is a platform for Massive Open Online Courses (MOOC). It is developed as an open source software, allowing any institution to use it and change its code.

## Installation Guide
This installation guide was based on Ubuntu 14.04 (trusty tar). However, other Linux versions can be used.  
It is recommended to run Tim Tec using NGINX as a web server and [uwsgi](https://uwsgi-docs.readthedocs.org/en/latest/) as proxy.  
This guide will follow a step-by-step installation. However, in Tim Tec’s GIT Repository, inside the folder “scripts”, there are two shell scripts: bootstrap-ubuntu.sh e production-ubuntu.sh. These scripts will execute the same steps described below.  
It is strongly suggested that the user performing the installation is not the root user. This guide will be performed using a new user: **timtec-production**. Should another user install Tim Tec, replace the user name on the commands bellow, when required.  
Also, both scripts use **timtec-production** as the user who will execute the proxy (uwsgi). Should another user run the scripts, open the file Makefile and change the user name on it.  
Please note that the user performing the installation must have sudo permissions.

Its possible if the timtec-production user already exists with the command:

    grep timtec-production /etc/passwd

Is the users just exists, the command above will return a line like this:

    timtec-production:x:999:999::/home/timtec-production:

If the users doesn't exist is possible create it with:

    sudo useradd --groups sudo --create-home --password <some password> timtec-production



### Install Git

Git is a system for revision control and source code management. GitHub, a web based Git repository, hosts Tim Tec’s source code. Therefore, in order to download Tim Tec, you will also need Git.  
Download and install Git:

    sudo apt-get -y install git

Then clone the GIT repository for Tim Tec:

    git clone https://github.com/hacklabr/timtec.git

### Dependencies

First, download Tim Tec’s dependencies:

    sudo apt-get update 
    sudo apt-get install -y git libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv

## Installing Nodejs

### Ubuntu

    sudo apt-get install -y nodejs npm

It is important to notice that Ubuntu use node as nodejs, so in order to guaranty Time Tec’s scripts compatibility with Ubuntu, it is necessary to create the following link:  

    sudo update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10

### Debian

    apt-get curl
    curl -sL https://deb.nodesource.com/setup | bash -
    apt-get install nodejs

For more information please refer to the [following link](https://github.com/joyent/node/wiki/installing-node.js-via-package-manager#debian-and-ubuntu-based-linux-distributions)

### Database
The default recommended database management system is Postgresql. However, django supports any Relational Databases. First, install Postgresql as the database management system:

    sudo apt-get install -y postgresql

Then, create a user (**timtec-production**) on postgresql:

    sudo su - postgres -c "createuser -d timtec-production" 

Finally, create the database:

    createdb --encoding "UTF-8" --locale "pt_BR.UTF-8" timtec-production

### Python Virtual Environment and Javascript Dependencies
Create a local config file:

    cp -a timtec/settings_local.py.template timtec/settings_local.py

Edit the created file `timtec/settings_local.py` and search for TODO sections to configure all the important parameters. **The system wil not work correctly if this file is not set up properly**.

Now, create a virtual environment for Python and also install the dependencies for python and nodejs. The following command will perform every step automatically, however, this guide contains the manual process, if necessary.

    make create-production

The script may prompt you asking for timtec-productions’s sudo password. Should any errors occur, please run the make command again, since most of the errors may be caused by problems with internet connection.

### Creating the Virtual Environment Manually (Optional, use this or do: make create-production)
First, create Python’s virtual environment:

    virtualenv /home/timtec-production/env
    source /home/timtec-production/env/bin/activate

Afterwards, install the dependencies:

    cd timtec
    make

The script may prompt you asking for timtec-productions’s sudo password. Should any errors occur, please run the make command again, since most of the errors may be caused by problems with internet connection.

### Web Server and Application Server
First, install NGINX and UWSGI:

    sudo apt-get install -y nginx uwsgi uwsgi-plugin-python

Now, configure UWSGI adding a file named **timtec-production.ini** to the UWSGI configuration folder at **/etc/uwsgi/apps-available/**. An example of this configuration file can be found at Tim Tec’s directory. Copy this example and change the necessary information:

    sudo cp scripts/conf/timtec-production.ini /etc/uwsgi/apps-available/ 
    sudo ln -s /etc/uwsgi/apps-available/timtec-production.ini /etc/uwsgi/apps-enabled/timtec-production.ini
    sudo service uwsgi start

Now, configure NGINX adding a file named **timtec-production** to the NGINX configuration folder at **/etc/nginx/sites-enabled/**. Tim Tec’s directory contains an example of this configuration file. Copy this example and change the necessary information:

    sudo cp timtec/scripts/conf/nginx-timtec-production /etc/nginx/sites-available/timtec-production
    sudo ln -s /etc/nginx/sites-available/timtec-production /etc/nginx/sites-enabled/timtec-production
    sudo rm /etc/nginx/sites-enabled/default
    sudo nginx -s reload

Then, edit both nginx and django configuration files, setting your domain information. Nginx’s configuration file can be found at: _/etc/nginx/sites-enabled/_  
_Django’s_ configuration file can be found at: _/home/timtec-production/settings_production.py_. In this file, change ALLOWED_HOSTS variable, defining it with your domain. Only domains listed on this variable can access the application. For local access add localhost as one of the values for the variable.  
After configuring the domain’s information, run:

    make update-production

Then, to update nginx configurations:

    sudo nginx -s reload

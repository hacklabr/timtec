Ambiente de desenvolvimento
===========================

Obtendo o timtec
----------------

::

    mkdir -p ~/dev
    cd dev
    git clone git clone git@github.com:hacklabr/timtec.git
    cd timtec

Dependências do SO
------------------

::

    # Pacote do archlinux
    sudo pacman -Sy python2 python-virtualenvwrapper postgresql nodejs

    sudo systemctl enable postgresql
    sudo systemctl start postgresql

    sudo su - postgres -c "initdb --locale pt_BR.UTF-8 -D '/var/lib/postgres/data'"
    sudo su - postgres -c "createuser -d $USER"
    createdb timtec

Obtendo bibliotecas
-------------------

Aqui estamos prssupondo que você está usando o Virtualenvwrapper (https://wiki.archlinux.org/index.php/Python/Virtualenv)

::

    mkvirtualenv -p /usr/bin/python2 timtec
    workon timtec
    

Configuração da aplicação
-------------------------

::

    cp timtec/settings_local.py.template timtec/settings_local.py
    # Altere o arquivo settings_local.py para entrar no banco.
    make
    ./manage.py changepassword admin

Rodar o servidor de teste
-------------------------

::

    ./manage.py runserver

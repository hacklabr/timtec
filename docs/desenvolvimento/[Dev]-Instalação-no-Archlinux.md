# Ambiente de desenvolvimento


## Obtendo o timtec
```
$ mkdir -p ~/devel
$ cd devel
$ git clone git@github.com:hacklabr/timtec.git
$ cd timtec
```


## Dependências do SO
```
$ sudo pacman -S 
$ sudo pacman -S python-virtualenvwrapper
$ sudo pacman -S postgresql
$ sudo pacman -S nodejs

$ sudo systemctl enable postgresql
$ sudo systemctl start postgresql

$ sudo su - postgres -c "initdb --locale pt_BR.UTF-8 -D '/var/lib/postgres/data'"
$ sudo su - postgres -c "createuser -d $USER"
$ sudo su - postgres -c "createdb --owner=$USER timtec"
```


## Obtendo bibliotecas
```
$ mkvirtualenv -p /usr/bin/python2 timtec
$ workon timtec
$ pip install -r requirements.txt
$ pip install -r dev-requirements.txt
$ sudo npm install -g less
```    

## Configuração da aplicação
```
$ cp timtec/settings_local_dev.py timtec/settings_local.py
$ ./manage.py syncdb --all --noinput
$ ./manage.py loaddata -i prod
$ ./manage.py changepassword admin
```
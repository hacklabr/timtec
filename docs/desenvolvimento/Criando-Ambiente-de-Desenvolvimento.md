# Criando Ambiente de desenvolvimento


O jeito mais fácil de obter o ambiente de desenvolvimento é usando o Vagrant (colocar link).

## Usando Vagrant
```
vagrant up
```
Pronto!

Você pode acessar o timtec no endereço http://localhost:8000 pelo seu navegador.

O super usuário do ambiente de teste é:

login: admin

senha: admin

Veja o Vagrantfile na raiz do repositório para maiores detalhes.

## Usando docker
Documentar aqui como usar o docker


# Criando Ambiente de desenvolvimento manualmente

## Obtendo o timtec
```
$ git clone git@github.com:hacklabr/timtec.git
$ cd timtec
```


## Dependências do Sistema Operacional


### Arch Linux

```
$ sudo pacman -S
$ sudo pacman -S python-virtualenvwrapper
$ sudo pacman -S postgresql
$ sudo pacman -S nodejs

$ sudo systemctl enable postgresql
$ sudo systemctl start postgresql

$ sudo su - postgres -c "initdb --locale pt_BR.UTF-8 -D '/var/lib/postgres/data'"
```

### Ubuntu 14.04 ou Debian 7 ou maior

```
sudo apt-get update
sudo apt-get install -y libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv git

sudo apt-get install -y postgresql

curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get update
sudo apt-get install -y nodejs

sudo update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10
```

## Criando e configurando o Banco de Dados no Postgress

```
$ sudo su - postgres -c "createuser -d <user>"
$ createdb timtec
```

## Obtendo bibliotecas

```
$ virtualenv -p /usr/bin/python2 env
$ source env/bin/activate
$ pip install -r requirements/test.txt
```

## Configurando ambiente de testes e instalando dependências do python (pip), node e bower

### Método automágico

Para fazer tudo automaticamente, execute o comando abaixo. Para mais detalhes, consulte o arquivo
Makefile na raiz do repositórios
```
    $ make
```

### Método Manual

#### Instalando dependências Python
```
$ pip install -r requirements/test.txt
```

#### Configurando testes
```
$ python setup.py -q develop
```

#### Instalando dependências Node
```
$ npm install
```

#### Instalando dependências javascript com bower
```
$ ./node_modules/bower/bin/bower install
```

## Django

### Configurando o Django
```
$ cp timtec/settings_local.py.template_dev timtec/settings_local.py
```

### Criando banco de dados e carregando dados iniciais
```
$ ./manage.py migrate
$ ./manage.py loaddata initial
```
### Criando super usuário

```
$ ./manage.py createsuperuser
```

## Rodando o servidor de teste
```
./manage.py runserver
```
Você pode acessar o timtec no endereço http://localhost:8080 pelo seu navegador.

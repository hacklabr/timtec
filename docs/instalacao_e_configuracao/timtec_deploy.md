Essa é a documentação básica de instalação (deploy) timtec. Para informações sobre requisitos e dependências, veja o [README.md](https://github.com/hacklabr/timtec/blob/master/README.md).

## Prepare o servidor

Você precisa de um servidor com algum dos seguintes sistemas operacionais:

* Ubuntu 14.04, 16.04 
* Debian 8.0

Certifique-se de ter a senha ssh deste servidor para começar o processo e de ter permissão de sudo(root) na máquina em questão. 

## Crie o usuário da aplicação

Sugerimos que o usuário usado para fazer a instalação não seja o root. Aqui, o usuário que está fazendo a instalação é o **timtec-production**. Assim, nos comandos abaixo, substitua o nome do usuário pelo que você estiver usando. Os scripts possuem uma variável para definir o usuário que executará o proxy (wsgi). Caso use um usuário diferente, olhe o arquivo Makefile e faça as alterações necessárias.

Este tutorial pressupões que você esteja logado com o usuário timtec-production, que ele esteja no grupo sudo.

É possível verificar se o usuário timtec-production existe através do comando:
```
root@server# grep timtec-production /etc/passwd
```

Caso o usuário exista, o comando acima deve retornar uma linha semelhante a seguinte:
```
timtec-production:x:999:999::/home/timtec-production:
```
Caso não exista é possível criá-lo com:

```
root@server# useradd --groups sudo --create-home timtec-production
```
Depois mude a senha:

```
root@server# passwd timtec-production
```

Se você estiver usando Debian, pode acontecer do sistema criar uma instância do novo usuário com acesso a um terminal sh. Se você quiser usar o bash (terminal mais completo e com mais funcionalidades), você pode alterar essa informação no arquivo de configuração de usuários. Proceda da seguinte maneira: 

1) Abra o arquivo /etc/passwd e verifique a linha onde está o usuário timtec-production. Você pode ver uma linha assim:    
```
timtec-production:x:1001:1001::/home/timtec-production:/bin/sh
```

2) Repare que a linha tem indicação para o terminal sh. Mude para bash e salve o arquivo com a linha desta maneira (use vim, nano ou qualquer editor de sua preferência): 
```
timtec-production:x:1001:1001::/home/timtec-production:/bin/bash
```

## Obtendo o código

Se você estiver usando Debian, pode acontecer do sistema criar uma instância do novo usuário com acesso a um terminal sh. Se você quiser usar o bash (terminal mais completo e com mais funcionalidades), você pode alterar essa informação no arquivo de configuração de usuários. Proceda da seguinte maneira:

1) Abra o arquivo /etc/passwd e verifique a linha onde está o usuário timtec. Você pode ver uma linha assim:    
```
     timtec:x:1001:1001::/home/timtec:/bin/sh
```
2) Repare que a linha tem indicação para o terminal sh. Mude para bash e salve o arquivo com a linha desta maneira (use vim, nano ou qualquer editor de sua preferência):

     timtec:x:1001:1001::/home/timtec:/bin/bash

* Atualize o índice de pacotes e instale o git

```
root@server# apt-get update
root@server# apt-get install git
```

* Com usuário da aplicação - no nosso caso timtec-production - faça a clonagem do repositório:

```
timtec-production@server$ git clone ~/https://github.com/hacklabr/timtec.git
```

Em seguida, escolha a versão desejada e atualize o código para ela com o comando abaixo. Aqui você encontra uma lista de versões do TIMTec: https://github.com/hacklabr/timtec/releases
```
timtec-production@server$ cd timtec
timtec-production@server$ git checkout <tag-da-versão>
```

Substitua a tag da versão por uma tag do git válida. Ex: `git checkout v4.0`

## Dependências
Primeiro, vamos instalar as dependências:

```
root@server# apt-get update
root@server# apt-get install -y libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv
```

### Instalando o nodejs

#### Ubuntu
```
root@server#  apt-get install -y nodejs npm
```

Diferente de todas as outras distribuições, o ubuntu usa o comando node para o nodejs por padrão, então vamos fazer isso:
```
root@server# update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10
```

#### Debian
```
root@server# apt-get install curl
root@server# curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
root@server# apt-get install nodejs
```

Mais informações [neste link](https://github.com/joyent/node/wiki/installing-node.js-via-package-manager#debian-and-ubuntu-based-linux-distributions)

### Banco de dados
Recomendamos o postgreSQL, mas o django suporta outros bancos de dados relacionais.
```
root@server# apt-get install -y postgresql
root@server# sudo su - postgres -c "createuser -d timtec-production"
```

Com usuário da aplicação, crie então a base:
```
timtec-production@server$ createdb --encoding "UTF-8" --locale "pt_BR.UTF-8" timtec-production
```
obs: caso ocorra algum problema relacionado a locale faltante no sistema, [veja como alterar o locale para pt_BR](Alterando-locale-para-pt_BR.md). 

### Ambiente virtual python e dependências de javascript

Em seguida, vamos criar o ambiente virtual python e instalar as dependências do python e do nodejs. O comando abaixo automatiza todo este processo, mas deixamos abaixo a opção manual.

```
$ cd ~/timtec
$ make install
```

Se ocorrer algum erro, tente rodar o comando make novamente, pois falhas podem ocorrer devido a problemas com a internet.

### Criando ambiente virtual manualmente
Em seguida, vamos criar o ambiente virtual python:

    $ virtualenv /home/NOME-DO-SEU-USUARIO-OU-DIRETORIO/env
    & source /home/NOME-DO-SEU-USUARIO-OU-DIRETORIO/env/bin/activate

Se você estiver seguindo a documentação, você pode deverá dar o comando da seguinte maneira:

    $ virtualenv /home/timtec-production/env
    $ source /home/timtec-production/env/bin/activate

Agora vamos instalar as dependências:

    cd timtec
    make install

Se ocorrer algum erro, tente rodar o comando make novamente, pois falhas podem ocorrer devido a problemas com a internet.


### Servidor web e de aplicação

Instale o servidor web (nginx) e o servidor de aplicação (uwsgi):

    $ sudo apt-get install -y nginx uwsgi uwsgi-plugin-python

Na pasta timtec/scripts/conf temos exemplo de arquivos de configuração. Copie os mesmos para seus locais e edite-os confore sua necessidade:

    $ sudo cp ~/timtec/scripts/conf/timtec-production.ini /etc/uwsgi/apps-available

Crie um link simbólico de apps-available para apps-enable:

    $ sudo ln -s /etc/uwsgi/apps-available/timtec-production.ini /etc/uwsgi/apps-enabled/timtec-production.ini

Inicie o serviço do servidor de aplicação:

    $ sudo service uwsgi start

Copie os scritps de configuração da instância timtec-production para os sites available do nginx:

    $ sudo cp ~/timtec/scripts/conf/nginx-timtec-production /etc/nginx/sites-available/timtec-production

Crie link simbólico do projeto de sites-available para sites-enable:

    $ sudo ln -s /etc/nginx/sites-available/timtec-production /etc/nginx/sites-enabled/timtec-production

Remova o arquivo de configuração padrão do nginx para não haver conflito:

    $ sudo rm /etc/nginx/sites-enabled/default

Faça um reload do nginx para se certificar que ele está rodando corretamente:

    # sudo nginx -s reload

Obs: se o nginx não estiver rodando, execute:

   $ sudo service nginx start

Em seguida, edite o arquivo de configuração do nginx para colocar seu domínio.

A instalação não terminou ainda! Precisamos criar o usuário inicial, configurar o domínio do django, o envio de email e a API do youtube.

Proceda a página de [Configurações](Configurações.md) para continuar.

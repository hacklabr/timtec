## Atualizando para uma nova versão

### 1. Verifique qual é a sua versão

* 1.1. As versões do TIMTec estão disponíveis aqui: https://github.com/hacklabr/timtec/releases Cada versão do TIMTec é uma tag no repositório git.
* 1.2. No seu servidor, logado com usuário da aplicação (se você seguiu a documentação deve ser o usuário timtec-production), entre na pasta da aplicação e de um git status:

```
timtec-production@server:$ git status
HEAD detached at v3.2
```

### 2. Baixe as atualizações e mude o checkout
No seu servidor, logado com usuário da aplicação (se você seguiu a documentação deve ser o usuário timtec-production), entre na pasta da aplicação e de um git pull:

```
timtec-production@server:$ git checkout master
timtec-production@server:$ git pull --all
timtec-production@server:$ git checkout v3.3
```
### 3. Faça o update

* 3.1 tive o ambiente virtual python:

```
timtec-production@server:$ virtualenv /home/NOME-DO-SEU-USUARIO-OU-DIRETORIO/env
timtec-production@server:$ source /home/NOME-DO-SEU-USUARIO-OU-DIRETORIO/env/bin/activate
```

Se você estiver seguindo a documentação, você pode deverá dar o comando da seguinte maneira: 
```
timtec-production@server:$ virtualenv /home/timtec-production/env
timtec-production@server:$ source /home/timtec-production/env/bin/activate
```

* 3.2 Rode o make update na pasta da aplicação:
```
timtec-production@server:$ cd ~/timtec/
timtec-production@server:$ make update
```

Feito isso, o software estará atualizado.

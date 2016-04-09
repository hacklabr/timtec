Ao tentar criar a base de dados, caso você receba um erro como este: 

```
createdb: database creation failed: ERROR:  invalid locale name: "pt_BR.UTF-8"
```

Você precisa instalar o locale pt_BR.UTF-8 em seu sistema. 

## Adicione locale

1 - Como root, adicione a entrada pt_BR ao arquivo /var/lib/locales/supported.d/local:
```
# echo "pt_BR pt_BR.UTF-8" >> /var/lib/locales/supported.d/local
```

2 - Também como root, adicione o alias pt_BR em /etc/locale.alias:
```
# echo "pt_BR pt_BR.UTF-8" >> /etc/locale.alias
```

3 - Modifique o locale padrão nos arquivos /etc/environment e /etc/default/locale e acrescente as linhas abaixo. Você também precisará de permissão de root:
```
LANG="pt_BR"
LANGUAGE="pt_BR:pt:en"
```
4 - Execute os seguintes comandos para gerar entradas dos locales inseridos no sistema:
```
# locale-gen
# update-locale LANG=pt_BR.UTF-8
```

5 - Reinicie o sistema para que tenha validade. 

Use o comando `locale` para ver a validade dos locales no sistema. Exemplo: 
```
# locale
LANG=pt_BR.UTF-8
LANGUAGE=pt_BR:pt:en
LC_CTYPE="pt_BR.UTF-8"
LC_NUMERIC="pt_BR.UTF-8"
LC_TIME="pt_BR.UTF-8"
LC_COLLATE="pt_BR.UTF-8"
LC_MONETARY="pt_BR.UTF-8"
LC_MESSAGES="pt_BR.UTF-8"
LC_PAPER="pt_BR.UTF-8"
LC_NAME="pt_BR.UTF-8"
LC_ADDRESS="pt_BR.UTF-8"
LC_TELEPHONE="pt_BR.UTF-8"
LC_MEASUREMENT="pt_BR.UTF-8"
LC_IDENTIFICATION="pt_BR.UTF-8"
LC_ALL=
```

## Modifique o template do postgres

1 - Como root, mude para o usuário `postgres` e entre no terminal `psql`
```
# su postgres
$ psql
```
2 - Como console `psql`, altere o `template1` dando update na base `pg_database`:
```
# update pg_database set datcollate = 'pt_BR.UTF-8', datctype = 'pt_BR.UTF-8' where datname='template1';
```

Pronto! Você alterou o locale padrão do seu sistema para pt_BR. 
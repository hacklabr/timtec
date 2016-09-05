#PT Br

## Documentação TIM Tec

Repositório do manual da aplicação [TIM Tec](https://github.com/hacklabr/timtec/). Para maiores informações, veja o portal do projeto: http://docs.timtec.com.br. 

Todos os documentos aqui são gerados com [mkdocs](http://www.mkdocs.org).  Esta documentação e a geração destes conteúdos está baseada em uma distribuição GNU/Linux usando gerenciador de pacotes apt. 

## Como compilar a documentação?  

1 - Instale o ambiente virtual python (python-virtualenv). Usarmos este ambiente para instalar o `mkdocs`. Permissões sudo ou root pode ser necessárias:

```
  # apt-get update
  # apt-get install python-virtualenv
```
2 - Crie e ative o ambiente virtual python

```
$ virtualenv docs-env
$ source docs-env/bin/activate
```
3 - Baixe a engine mkdocs via pip
```
$ pip install mkdocs
```

## Como usar mkdocs localmente? 

1 - Depois de clonar o repositório, entre na pasta docs e rode `mkdocs serve`. Veja:

```
$ cd docs
$ mkdocs serve
```
2 - No endereço padrão localhost + porta 8000 (127.0.0.1:8000) você pode ver o site em realtime. Se você quiser processa modificaçõe, o mkdocs mostrará em tempo real. 


## Gerando arquivos estáticos html/css/js 

1 - Para gerar uma documentação em formato html estruturado, vamos compilar essa documentação. Dentro da pasta /docs rode o comando `mkdocs build`: 

```
$ mkdocs build
```

Após esse processo será criado um novo diretório chamado `site`. Este conterá todos os arquivos da página. Dentro do diretório os arquivos estarão assim:

```
  user@Server:~/zup-docs$ ls -la site/
  total 80 files
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 api_configuration
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 css
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 fonts
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 images
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 img
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 implement
  -rw-r--r--  1 user user 7926 Nov 23 15:18 index.html
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 installation_docker
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 javascript
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 js
  drwxr-xr-x  3 user user 4096 Nov 23 15:18 license
  drwxr-xr-x  3 user user 4096 Nov 23 15:18 mkdocs
  -rw-r--r--  1 user user 4917 Nov 23 15:18 search.html
  -rw-r--r--  1 user user  990 Nov 23 15:18 sitemap.xml
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 updating_docker
  drwxr-xr-x  2 user user 4096 Nov 23 15:18 web_configuration
```

Para atualizar a documentação a partir de mudanças geradas nos arquivos .md, limpe os arquivos estáticos e gere novamente a documentação. 
```
$ mkdocs build --clean
$ mkdocs build
```

To more information about mkdocs, see [http://www.mkdocs.org](http://www.mkdocs.org/). 



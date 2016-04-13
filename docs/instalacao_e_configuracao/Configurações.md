## Configurações importantes pós instalação: 

1. Verifique seu arquivo `/timtec/timtec/settings_local.py`. A maioria das configurações de ambiente estará lá;
2. Configure uma chave de API do Youtube e de serviços de autenticação (ex.: facebook);
3. Configure seu serviço de envio de email. Veja sessão [Configurando Envio de E-mails(SMTP).md](Configurando Envio de E-mails(SMTP).md);

## Settings Local
Dentro da aplicação há um importante arquivo chamado settings_local.py que contém os principais parâmetros da ferramenta. Nele você deve: inserir a url que estará ativa em seu domínio, inserir sua chave de API do Youtube, conectar integração com Moodle, entre outros detalhes importantes. 

Este arquivo, depois da instalação seguida conforme o manual, estará dentro da pasta /timtec/timtec. Veja uma possibilidade de edição do mesmo:

```
$ vi ~/timtec/timtec/settings_local.py
```

Atente para o modelo deste arquivo aqui [settings_local.py](https://github.com/hacklabr/timtec/blob/master/timtec/settings_local.py.template).

É importante que, depois de editado, você rode os comandos pós-alterações abaixo. 

## Comandos importantes pós alterações

Quando fizer alterações, muitas vezes é importante reiniciar os principais serviços em uso. Tenha isso em mente toda vez que fizer alterações nos parâmetros da aplicação. 


#### Dando update na aplicação
Toda vez que dados forem mudados no arquivo de parametrização da aplicação, o update do Django tem de ser acionado. 

```
$ cd ~/timtec
$ make update
```

#### Reiniciando o NGINX
```
$ sudo nginx -s reload
```

#### Reiniciando o UWSGI
```
$ sudo service uwsgi stop
$ sudo service uwsgi start
```

## Criando um super usuário

1 - Ative o environment do Django: 

  `source /home/timtec-production/env/bin/activate`

2 - Crie um super usuário para a aplicação: 

`~/./timtec/manage.py createsuperuser`

3 - Se for necessário trocar a senha: 

`~/./timtec/manage.py changepassword LOGIN-DO-USUARIO`

Feito isso, você poderá acessar a [interface admin do django](https://docs.djangoproject.com/en/1.6/ref/contrib/admin/) pelo endereço <domínio>/django/admin. Exemplo (no browser): 

'http://sua-url//django/admin'

## Variáveis

A configuração se dá basicamente usando as variáveis definidas no módulo [settings do django](https://docs.djangoproject.com/en/1.8/ref/settings/). No caso do TIM Tec, temos o arquivo settings_local.py que é ignorado pelas atualizações do git. Isolamos neste módulo python as variáveis relevantes de configuração, pois o módulo settings define várias questões sobre o projeto django, como as apps django usadas.

Após realizar qualquer alteração neste arquivo settings_local.py, você deve executar o comando abaixo na home do usuário, para que as mudanças tenham efeito:

`touch wsgi-reload`

Se você for um usuário avançado, o arquivo settings.py que contém a maioria das definições sobre a plataforma fica em timtec/settings.py a partir da raiz do repositório.

## Tema

Definição o tema do TIM Tec. Atualmente temos 3 temas:

* **default**: tema neutro, padrão do software
* **timtec**: tema usado em timtec.com.br
* **ifs-colors**: tema desenvolvido para os Institutos Federais de Educação, Ciência e Tecnologia
* **if**: tema desenvolvido para o Institutos Federais de Educação, Ciência e Tecnologia

Basta colocar o valor de uma destas 3 strings acima na variável TIMTEC_THEME, ex:

`TIMTEC_THEME = 'default'`

## Autenticação

O django-allauth é usado para implementar a autenticação, e ele possui algumas variáveis de configuração. Ele é usado para configurar a autenticação usando o facebook.

Você pode verificar as variáveis suportadas [aqui](https://readthedocs.org/projects/django-allauth/)

Para configurar a autenticação via facebook, é preciso criar uma app no facebook, que possui documentação própria [aqui](https://developers.facebook.com/docs/javascript)

## Domínios permitidos

A Variável [ALLOWED_HOSTS](https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts) define para quais domínios a aplicação vai aceitar conexões (requests). Ex.:

`ALLOWED_HOSTS = [
    'localhost',
    'timtec.com.br',
    '.timtec.com.br',
]`

Se você estiver rodando a aplicação numa rede local e quiser que todos os ips da rede possam acessar a aplicação, pode colocar isto: 

`ALLOWED_HOSTS = ["*",
]`


## Configurações de email

Definidas principalmente pela variável [EMAIL_BACKEND](https://docs.djangoproject.com/en/1.6/ref/settings/#email-backend). Verifique a documentação do django sobre envio de emails para maiores detalhes: https://docs.djangoproject.com/en/1.6/topics/email/#email-backends

Caso a configuração de email esteja incorreta, ocorrerá um erro durante a criação de usuário.

## Upload de arquivos - NGINX
No arquivo **/etc/nginx/sites-available/NOME-DO-SITE.conf** o parâmetro **client_max_body_size** deve ter seu limite aumentado caso o ambiente precise receber arquivos de tamanhos acima de 4Mega. Normalmente **client_max_body_size 60m;** resolve para a importação do cursos já disponibilizados na Plataforma TIMTec.

## Configuração da chave da api do youtube
A chave da api do youtube serve para acessar informações sobre o Vídeo durante a criação das Unidades e do vídeo de introdução do curso.

SEM ESTA CHAVE, A ADMINISTRAÇÃO DO CURSO NÃO IRÁ FUNCIONAR CORRETAMENTE!!!
Veja como obter a chave da api do youtube neste link: https://developers.google.com/youtube/v3/getting-started?hl=pt-br

Após obter a chave, defina a configuração no arquivo settings_local.py:

`YOUTUBE_API_KEY = 'sua_chave_api_youtube'`

## Configurando conexão com Moodle
Ver sessão [[Autenticando no Timtec com OpenID do Moodle]] 

## Verificando Logs
Caso a aplicação apresente erros e/ou inconsistências, talvez seja importante verificar os logs. 

Log Nginx
```
$ sudo nano /var/log/nginx/production.timtec.com.br.error.log
$ sudo nano /var/log/nginx/production.timtec.com.br.access.log
```

Log UWSGI
```
$ sudo nano /var/log/uwsgi/app/timtec-production.log
```

## Configurando integração com Facebook

pendente


## Instruções de importação dos cursos
1. Considerando que você possui uma instalação da aplicação mais atual (ver Releases: https://github.com/hacklabr/timtec/releases) e quer utilizar os cursos disponíveis no projeto TIM Tec, logue no painel com permissão  no papel de administrador;

2. Acesse o repositório de curso e faça o download dos cursos que deseja importar: https://github.com/institutotim/timtec-cursos

3. Depois de baixar os pacotes com extensão .tar.gz, vá para o painel de administração da plataforma. Todos estes cursos compõe a primeira série de cursos do Projeto TIMTec. Depois de baixados estes arquivos podem ser importados através do caminho "Administração" > "Cursos" > "Importar Cursos", ou diretamente pelo endereço: http://sua-url/admin/courses

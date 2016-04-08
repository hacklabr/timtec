# Documentação TIM Tec

Repositório do manual da aplicação TIM Tec. Para maiores informações, veja o portal do projeto: http://timtec.com.br/


## Como compilar essa documentação


### Debian 8 (Jessie) ###

1. Instale os pacotes necessários

``
$ sudo apt-get install python-sphinx python-sphinx-rtd-theme
``

2. Clone este repositório

``
git clone https://github.com/institutotim/timtec-doc.git
``

3. Entre no diretório aonde está o **Makefile** e gere a documentação em html ou pdf

``
cd timtec-doc && make html
``

4. Para gerar a versão o PDF

``
make pdflatex
``


Caso seja necessário gerar novamente a documentação, limpe o diretório ``build`` ou use o comando abaixo:

``
make clean && make html
``

5. Dentro do diretório ``build`` há uma pasta chamada ``html``, envie para o servidor web e pronto!

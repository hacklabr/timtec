[![Stories in Ready](https://badge.waffle.io/institutotim/timtec.png?label=ready&title=Ready)](https://waffle.io/institutotim/timtec)
[![Build Status](https://drone.io/github.com/institutotim/timtec/status.png)](https://drone.io/github.com/institutotim/timtec/latest)

# TIM Tec

A plataforma de cursos online TIM Tec é um software livre desenvolvido pelo Instituto TIM que utiliza o conceito de MOOC (Massive Open Online Courses), cursos abertos e livres que podem ser feitos simultaneamente por muitas pessoas.

O sistema pode hospedar múltiplos cursos que utilizam videoaulas, além de materiais de apoio e outros links. A ferramenta permite a criação de testes e o uso de emuladores desenvolvidos para que alunos exercitem os conhecimentos abordados. Alunos podem fazer e responder perguntas, ver respostas e favoritar as perguntas dos colegas em um fórum, além de fazer anotações em seu caderno virtual. Gestores podem gerar relatórios de acompanhamento dos cursos, turmas e alunos, acompanhar o progresso de cada participante e habilitar professores tutores quando necessário.

A tecnologia e os conteúdos da plataforma TIM Tec estão sendo compartilhados com instituições públicas de ensino da Rede e-Tec Brasil, com o apoio da Secretaria de Educação Profissional e Tecnológica do Ministério da Educação (Setec/MEC). Entre as instalações já implementadas estão:

* Instituto Federal Sul-rio-grandense http://mooc.ifsul.edu.br/
* Instituto Federal do Paraná http://mooc.ifpr.edu.br/
* Instituto Federal Sul de Minas https://mooc.ifsuldeminas.edu.br/
* Instituto Federal do Acre http://mooc.ifac.edu.br/
* Instituto Federal Fluminense  http://mooc.iff.edu.br/
* Instituto Federal de São Paulo http://mooc.ifsp.edu.br/
* Instituto Federal de Santa Catarina http://mooc.ead.ifsc.edu.br/
* Instituto Federal do Amazonas http://mooc.ifam.edu.br/
* Instituto Federal de Minas Gerais – Campus Ouro Preto http://mooc.ifmg.edu.br/
* Instituto Federal Farroupilha http://mooc.iffarroupilha.edu.br/
* Instituto Federal do Tocantins http://mooc.ifto.edu.br/
* Instituto Federal Baiano http://mooc.ifbaiano.edu.br/

## Instalação e configurações
Para acessar a documentação completa, veja a pasta [docs](docs) na raiz da aplicação.

* [INSTALAÇÃO release v3.2 ou superior](docs/instalacao_e_configuracao/Instalação.md)
* [ATUALIZAÇÃO a partir v3.2 ou superior](docs/instalacao_e_configuracao/Atualização.md)
* [ATUALIZAÇÃO a partir da versão 3.0.10 ou inferior](docs/instalacao_e_configuracao/Atualizando-a-partir-da-versão-3.0.10-ou-inferior.md)
* [CONFIGURAÇÕES v3.2 ou superior](docs/instalacao_e_configuracao/Configurações.md)
* [CONFIGURAÇÕES (Versão 3.0.10 e inferiores)](docs/instalacao_e_configuracao/Configurações-(Versão-3.0.10-e-inferiores).md)


## Desenvolvimento
* [Criando ambiente de dev](docs/instalacao_e_configuracao/%5BDev%5D-Instalação-no-Archlinux.rst)
* [Temas](docs/instalacao_e_configuracao/Temas.md)
* [Tutorial para criação de tema](docs/instalacao_e_configuracao/Tutorial-para-criação-de-tema.md)


## Licença - AGPLV3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see LICENSE file here or
    [AGPLv3](http://www.gnu.org/licenses).

[![Build Status](https://drone.io/github.com/hacklabr/timtec/status.png)](https://drone.io/github.com/hacklabr/timtec/latest)
[![Coverage](https://coveralls.io/repos/hacklabr/timtec/badge.png)](https://coveralls.io/r/hacklabr/timtec)

## Requisitos de instalação

* Operating system: Debian (>= 7.7) or Ubuntu (14.04);
* Proxy server: uwsgi (>= 2.0.7);
* Web Server: nginx (>= 1.6.2);
* javascript server-side interpreter: node.js (>= 0.10.40);
* Data base server: postgresql (>= 9.2);
* Python language package: python (= 2.7 ou < 3);
* Virtual Enviroment Python: virtualenv (>=1.11.6);

## Requisitos de Desenvolvimento
* all the above requirements
* build essentials and many dev packages if on apt/rpm based systems
    * libpq-dev, libjpeg-dev, libpng12-dev, build-essential, python-dev, gettext
* nodejs (0.10+) (you will need a ppa for ubuntu < 14.04)

### Production Environment Requirements
#### UP to 6000 users
* Processor: Dual Core
* RAM: 2 to 4 GB
* Disk Space: 10 GB
* Network Total Transfer/mo: ~12GB
* Incoming: 1GB
* Outgoing: 11 GB

#### UP to 10k/12k users
* Processor: Quad Core
* RAM: 4 to 6 GB
* Disk Space: 25 GB
* Network Total Transfer/mo: ~25GB
* Incoming: 2GB
* Outgoing: 23 GB

### Python env
* create a Python 2.X virtualenv

    `virtualenv ../timtec-env`

* activate the virtual env

    `source ../timtec-env/bin/activate`

* run make

    `make`

* run the django devel server

    `./manage.py runserver`

### Getting Started

We provide a vagrant file for easy dev environment creation. Install
[Vagrant](http://www.vagrantup.com/) and on the main directory run:

    vagrant up

Them you just need to go inside the machine to start the dev server:

    vagrant ssh

On the VM console:

    ./manage.py runserver 0.0.0.0:8000

Now the system is running, you can go to `http://localhost:8000` on your web
browser and navigate on it.
To create a new superuser (so you can give permissions to other make other users professors) run:

    ./manage.py createsuperuser

See the Vagrantfile and script folder for more details.

## Running Tests

We made a bunch of tests for the system. They are separated into python tests
(that includes selenium full stack tests) and Karma/AngularJS tests. To run all
of them together just type

    make all_tests

remember that you need to have your virtualenv activated and has installed
everything from the `dev-requirements.txt` file.

### python

Activate virtual env, then:

    make python_tests

### Angular

In the root of repository:

    make karma_tests


### Suporte
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/hacklabr/timtec?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# Temas

Os arquivos javascript e as folhas de estilo (CSS) são minificados e compilados, respectivamente, usando o [django-pipeline](https://django-pipeline.readthedocs.org/en/latest/).

# Templates Django
O TIM Tec usa o framework web Django, e no _frontend_ a [linguagem de template Django (Django template language)](https://docs.djangoproject.com/en/1.6/topics/templates/), que é projetada para ser confortável para pessoas acostumadas a trabalhar com HTML. Ela é a camada de apresentação, constituída de variáveis, filtros e **tags**, isolada da camada lógica, escrita em python.

Está além desta documentação explicar o funcionamento da sintaxe da linguagem de template Django, amplamente documentada pelo próprio Django.

# Estrutura de Templates
Os templates do TIM Tec estão na pasta [themes](https://github.com/hacklabr/timtec/tree/master/themes) do repositório e cada pasta dentro dela é um tema.

O tema default é o tema base do timtec. Segue abaixo a lista de templates do diretório [themes/default/templates](https://github.com/hacklabr/timtec/tree/master/themes/default/templates), comentando cada um deles.

## base.html

Quase todos os templates (com exceção dos começado por "_") [extendem o template](https://docs.djangoproject.com/en/1.6/topics/templates/#template-inheritance) base.html. Nele é criado a estrutura básica do HTML, e nele são declaradas as tags `<head>` e `<body>`. Este template também define os principais [blocos](https://docs.djangoproject.com/en/1.6/topics/templates/#template-inheritance) e usa a [tag include](https://docs.djangoproject.com/en/1.6/ref/templates/builtins/#include) para inserir o cabeçalho (header.html) e o rodapé (footer.html), que serão vistos mais adiante.

## Herança de Templates
Usamos a [herança de templates do django](https://docs.djangoproject.com/en/1.6/topics/templates/#template-inheritance) para evitar repetição no código. Para isso, usamos a tag extends, e sobrescrevemos os blocos (definidos pela tag block) que desejamos. O template base.html tem dois blocos importantes: o content, onde vão os conteúdos da página, e o block js, usado para incluir arquivos javascritp específicos para cada página.

## header.html
![Header](http://i.imgur.com/8mb61or.png)

## home.html
![Home](http://i.imgur.com/Nf0GJer.png)

## forum.html
![Forum](http://i.imgur.com/3y3BKS7.png)

## account
* login.html
![Login](http://i.imgur.com/gKOYBZV.png)

* password_reset_from_key.html
![Password Reset Form](http://i.imgur.com/5wqtwjy.png)

## administration
* course-material-admin.html
![Course Material Admin](http://i.imgur.com/h1PNYUv.png)

* courses.html
![Courses](http://i.imgur.com/CiHFFLp.png)

## core
## flatpages
## metron
## socialaccount
## _admin_header_inline.html
## _contact_form.html
## _course-details-inline.html
## _course-header-inline.html
## _course_authors_inline.html
## _course_professors_modal.html
## _courses_aside.html
## _create_class_modal.html
## _forum_inline.html
## _highlight.html
## _lesson_header.html
## _login_modal.html
## _modal_about.html
## _notes_inline.html
## _signup_modal.html
## accept-terms.html
## class_edit.html
## classes.html
## course-material.html
## course-notes.html
## course.html
## courses.html
## empty.html
## footer.html
![Footer](http://i.imgur.com/0L6ayW6.png)

## lesson.html
## message.html
## messages.html
## notes.html
## profile-edit.html
## profile.html
## question-create.html
## question.html
## user-courses.html


## Estrutura das folhas de estilos (less)

O Timtec utiliza o [Bootstrap](https://github.com/twbs/bootstrap) como framework base bem como [Less](https://github.com/less/less.js) para escrever e pré-processar os estilos (CSS) dos temas.  

A estrutura de arquivos apresenta-se conforme abaixo:

    tema/
    |-- static/
        |-- css/
            |-- less/
                |-- components/      
                |   |-- ...   # componentes reaprovetáveis
                |               da interface
                |-- modules/         
                |   |-- ...   # módulos básicos da interface 
                |   
                |-- pages/           
                |   |-- ...   # estilos específicos de páginas
                |               e áreas do site
                |               
                |-- main.less # arquivo que importa e compila
                                todos os outros arquivos    

O arquivo `main.less` do tema padrão importa o arquivo principal do Bootstrap bem como os demais arquivos Less do tema.

O arquivo `settings.less` na pasta `modules` é o que sobreescreve as variáveis do Bootstrap que forem necessárias, bem onde estão as variáveis específicas do tema.

A estrutura de pasta é a mesma no tema padrão e nos demais temas, que importam o arquivo `main.less` do tema padrão para que ele seja usado como base.

Quando alguma modificação na interface é necessária, é recomendado manter a mesma estrutura de arquivos do tema base, ou seja, para alterar as variáveis Less do projeto cria-se um `settings.less` da mesma forma que existe no tema padrão, para modificar algum elemento da página de cursos cria-se o arquivo `courses.less` na pasta `pages`, e assim por diante.

## O Tema padrão

## Criando um novo tema

## Configurando o tema

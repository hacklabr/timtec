# coding: utf-8

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def initial_dev_data():
    from ..models import (
        User,
        Course,
        Lesson,
        CourseProfessors,
        Video,
        Block,
        Activity,
    )
    with transaction.manager:
        course = Course()
        course.slug = u'dbsql'
        course.name = u'Introdução ao Banco de Dados'
        course.description = u''
        course.abstract = (
            u'<p>Introdução aos conceitos fundamentais de bancos de dados modernos, desde a forma de organização dos dados (modelos e esquemas de dados) até comandos fundamentais da linguagem SQL e noções de projeto de bancos de dados normalizados. Noções de arquitetura de sistemas, gerenciadores de nacos de dados, integridade referencial, linguagens de definição, manipulação e controle de dados, além de tratar das questões de segurança, integridade e controle de transações.</p>'
            u'<p><strong><i class="icon-list"></i> Estrutura do curso:</strong>'
            u'<br>Vídeo-aulas (12 horas)'
            u'<br>Testes On Line'
            u'<br>Leitura de material didático de apoio'
            u'<br>Exercícios individuais de aplicação</p>'
        )

        course.knowledge_acquired = (
            u'Banco de dados são empregados em praticamente todos os sistemas Web, desde redes sociais a portais de comércio eletrônico, bem como aplicativos comerciais.'
        )
        course.knowledge_required = (
            u'O interessado deverá possuir conhecimentos básicos (selecionar, copiar, colar, criar pastas, salvar e renomear documentos) de algum sistema operacional e de navegação na Internet. '
            u'Para participar deste curso e realizar seus exercícios é necessário um computador com acesso à internet, navegador web atualizado (pelo menos 2) e algum programa de edição de texto sem formatação. '
            u'É recomendada a idade mínima de 14 anos.'
        )
        
        course.time_estimated = (
            u'<p><strong><i class="icon-time"></i> Carga horária:</strong> <br/>40 horas, a serem completadas em seis semanas</p>'
            u'<p><small>O tempo estimado de dedicação do aluno e agenda de comprometimento sugerida são de 12 horas de aulas expositivas, a serem completadas em 6 semanas e a sugestão de dedicação do aluno é de 6 horas por semana, sendo 2hrs para assistir aulas e 4hrs para fazer exercícios</small></p>'
        )
        course.extra_dadication = (
            u'<hr/>'
            u'<p><strong>Relação do curso com o PRONATEC:</strong></p>'
            u'<p>Eixo Tecnológico: Informação e Comunicação</p>'
            u'<p>Títulos semelhantes oferecidos Guia PRONATEC:</p>'
            u'<ul>'
            u'<li>Técnico em Informática</li>'
            u'<li>Técnico em Manutenção e Suporte em Informática</li>'
            u'<li>Técnico em Informática para Internet</li>'
            u'</ul>'
            u'<p>Títulos semelhantes oferecidos Guia PRONATEC de cursos FIC:</p>'
            u'<ul>'
            u'<li>Administrador de Banco de Dados</li>'
            u'<li>Operador de Computador</li>'
            u'<li>Programador de Dispositivos Móveis</li>'
            u'<li>Programador de Sistemas</li>'
            u'<li>Programador Web</li>'
            u'</ul>'
            u'<p>Outros nomes atribuídos a estes profissionais:</p>'
            u'<ul>'
            u'<li>Técnico em Formação de Instrutores de Informática</li>'
            u'<li>Técnico em Planejamento e Gestão em Tecnologia da Informação</li>'
            u'</ul>'
        )

        lessons = [
            (1, u'Aula 1: Modelos de dados e introdução ao modelo relacional', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis.'),
            (2, u'Aula 2: Introdução a SQL (demonstração), SGBDs e definição de esquemas', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (3, u'Aula 3: SELECT, Projeção x seleção e uso do console', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (4, u'Aula 4: Seleções com lógica booleana', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (5, u'Aula 5: Chaves: simples, compostas, candidatas, primárias, estrangeiras, mudas', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (6, u'Aula 6: Consultas com relacionamentos, joins implícitos e explícitos', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (7, u'Aula 7: Consultas com agregação', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (8, u'Aula 8: Operações de alteração de dados e transações', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (9, u'Aula 9: Projeto de bancos de dados normalizados e formas normais', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (10, u'Aula 10: Índices e constraints', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (11, u'Aula 11: Triggers e views, dialetos de SQL entre SGBDs importantes', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!'),
            (12, u'Aula 12: Limitações e alternativas ao modelo tradicional', u'Pellentesque augue sit dapibus sociis magna amet cras mattis egestas, elementum placerat sagittis!')
        ]

        for position, lesson_title, lesson_desc in lessons:
            lesson = Lesson()
            lesson.position = position
            lesson.name = lesson_title
            lesson.desc = lesson_desc
            course.lessons.append(lesson)
            if lesson.position == 1:
                lesson1 = lesson
            DBSession.add(lesson)

        user_andersonorui = User(username="andersonorui", password="asdf", email="andersonorui@hacklab.com.br", name="Anderson Orui")
        DBSession.add(user_andersonorui)

        professor_1 = User(username='ramalho', password='kdkdk', email='skdsk@vcx')
        professor_1.name = u'Luciano Ramalho'
        DBSession.add(professor_1)

        course_professor = CourseProfessors()
        course_professor.user = professor_1
        course_professor.biography = (
            u'Luciano Ramalho é sócio e professor nas Oficinas Turing. Foi diretor técnico do Brasil Online, primeiro portal da Abril S/A na Web. Liderou times para os portais IDG Now, BOL, UOL, AOL Brasil e outros, usando Python desde 1998. Como instrutor, atendeu clientes como Citibank, CPqD, Serpro, Presidência da República, Globo.com e Itaú. Ajudou a criar a Associação Python Brasil e foi seu presidente. É membro da Python Software Foundation e fundador do Garoa Hacker Clube, o primeiro hackerspace do Brasil. Já palestrou várias vezes em eventos internacionais como FISL, OSCON e PyCon US.'
        )
        DBSession.add(course_professor)
        course.professors.append(course_professor)

        DBSession.add(course)

        # Create blocks
        activity1 = Activity()
        activity1.title = u'Exercício multipla escolha1'
        activity1.type = u'multiplechoice'
        activity1.data = u'{question: "Este é um exemplo de teste de multipla escolha", choices: ["Esta escolha é boa!", "Esta também é esperada", "Esta obviamente não é a a correta"]}'
        activity1.espected_answer_data = u'{choices: [0, 1]}'
        DBSession.add(activity1)

        activity2 = Activity()
        activity2.title = u'Exercício multipla escolha2'
        activity2.type = u'singlechoice'
        activity2.data = u'{question: "Este é um exemplo de teste de multipla escolha", choices: ["Esta escolha é boa!", "Esta não.", "Esta obviamente não é a a correta"]}'
        activity2.espected_answer_data = u'{choice: 1}'
        DBSession.add(activity2)


        video1 = Video()
        video1.name = u'Video 1 de teste'
        DBSession.add(video1)

        video2 = Video()
        video2.name = u'Video 2 de teste'
        DBSession.add(video2)

        video3 = Video()
        video3.name = u'Video 3 de teste'
        DBSession.add(video3)

        video4 = Video()
        video4.name = u'Video 4 de teste'
        DBSession.add(video4)

        video5 = Video()
        video5.name = u'Video 5 de teste'
        DBSession.add(video5)

        video6 = Video()
        video6.name = u'Video 6 de teste'
        DBSession.add(video6)

        block1 = Block()
        block1.video = video1
        block1.position = 1
        block1.lessons.append(lesson1)
        DBSession.add(block1)

        block2 = Block()
        block2.video = video2
        block2.activity = activity2
        block2.position = 2
        block2.lessons.append(lesson1)
        DBSession.add(block2)

        block3 = Block()
        block3.video = video3
        block3.activity = activity1
        block3.position = 3
        block3.lessons.append(lesson1)
        DBSession.add(block3)

        block4 = Block()
        block4.video = video4
        block4.position = 4
        block4.lessons.append(lesson1)
        DBSession.add(block4)

        block5 = Block()
        block5.video = video5
        block5.position = 5
        block5.lessons.append(lesson1)
        DBSession.add(block5)

        block6 = Block()
        block6.video = video6
        block6.position = 6
        block6.lessons.append(lesson1)
        DBSession.add(block6)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    initial_dev_data()

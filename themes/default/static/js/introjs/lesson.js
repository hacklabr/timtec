function startIntro(){
    var intro = introJs();
    intro.setOptions({
        showStepNumbers: false,
        overlayOpacity: 0.6,
        nextLabel: 'Próximo',
        prevLabel: 'Anterior',
        skipLabel: 'Pular',
        doneLabel: 'Pronto',
        steps: [
            {
                intro: 'Página das aulas'
            },
            {
                element: '#lesson-list-dropdown',
                intro: 'Menu com a lista de aulas',
                position: 'bottom'
            },
            {
                element: '#lesson-units-nav',
                intro: 'Conjunto de capítulos de uma aula',
                position: 'right'
            },
            {
                element: '#student-notes',
                intro: 'Área para anotações do aluno',
                position: 'left'
            },
            {
                element: '#materials',
                intro: 'Área para materiais adicionais',
                position: 'top'
            },
            {
                element: '#forum',
                intro: 'Fórum do curso',
                position: 'top'
            },
            {
                element: '#course-nav',
                intro: 'Menu para acessar cada uma das áreas e o caderno virtual',
                position: 'bottom'
            },
            {
                element: '#admin-link',
                intro: 'Administração dos cursos',
                position: 'bottom'
            }
        ]
    });

    intro.start();
}

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
                intro: 'Página inicial de um curso'
            },
            {
                element: '#course-video',
                intro: 'Vídeo de apresentação do curso',
                position: 'right'
            },
            {
                element: '#instructors-info',
                intro: 'Currículo do professor',
                position: 'left'
            },
            {
                element: '#lesson-list',
                intro: 'Estrutura do curso e lista das aulas',
                position: 'top'
            },
            {
                element: '#go-to-course',
                intro: 'Clique para iniciar o curso',
                position: 'bottom'
            }
        ]
    });

    intro.start();
}

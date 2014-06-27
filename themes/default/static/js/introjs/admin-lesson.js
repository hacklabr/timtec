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
                element: '#save-publish-buttons',
                intro: 'Botões para salvar e publicar aulas',
                position: 'bottom'
            },
            {
                element: '#video-activity-buttons',
                intro: 'Botões para inserir vídeos e atividades',
                position: 'bottom'
            }
        ]
    });

    intro.start();
}
function startIntro(){
    var intro = introJs();
    intro.setOptions({
        showStepNumbers: false,
        overlayOpacity: 0.4,
        nextLabel: 'Próximo',
        prevLabel: 'Anterior',
        skipLabel: 'Pular',
        doneLabel: 'Pronto',
        steps: [
            {
                element: '#site-brand',
                intro: 'Área para marca da Instituição',
                position: 'bottom'
            },
            {
                element: '#site-nav',
                intro: 'Menu superior',
                position: 'bottom'
            },
            {
                intro: 'Imagem de destaque',
                position: 'bottom'
            },
            {
                element: '#courses',
                intro: 'Área para cursos em destaque',
                position: 'top'
            },
            {
                element: '#how-it-works .container',
                intro: 'Área para instruções aos usuários',
                position: 'top'
            },
            {
                element: '.enroll',
                intro: 'Clique para ir ao curso',
                position: 'bottom'
            }
        ],
    });
    intro.setOption('doneLabel', 'Próxima página').start().oncomplete(function() {
      window.location.href = 'course/html5/intro/?multipage=true';
    });
}
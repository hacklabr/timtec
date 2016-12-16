(function(angular){
    'use strict';

    var app = angular.module('ui.tinymce');

    // If you want to cutomize uiTinymceConfig for your theme, please copy this file to you theme in the
    // same path (static/js/). This are the default setting for timtec
    app.value('uiTinymceConfig', {
        base_url: '/static/tinymce-dist/',
        related_url: true,
        inline: false,
        menubar: false,
        statusbar: false,
        relative_urls: false,
        plugins : 'advlist lists autolink link image media',
        toolbar: 'bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | quicklink link image media fullscreen',
        skin: 'lightgray',
        theme : 'modern',
        language: 'pt_BR',
        language_url : '/static/vendor/tinymce/langs/pt_BR.js',

        // media customizations
        media_poster: false,
        media_alt_source: false,
        media_dimensions: false,
        media_url_resolver: function (data, resolve/*, reject*/) {
            var complete_url = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            var result = complete_url.exec(data.url);
            if (result && result[2].length == 11) {
                var youtube_id = result[2];
                var embedHtml = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+ youtube_id +'" frameborder="0" allowfullscreen></iframe>';
                resolve({html: embedHtml});
            } else {
                resolve({html: ''});
            }
        },
    })

})(window.angular);

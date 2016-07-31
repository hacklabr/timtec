(function(angular){
    'use strict';

    var app = angular.module('ui.tinymce')

    // If you want to cutomize uiTinymceConfig for your theme, please copy this file to you theme in the
    // same path (static/js/). This are the default setting for timtec
    app.value('uiTinymceConfig', {
        inline: false,
        menubar: false,
        plugins : 'advlist autolink link image lists charmap print preview',
        toolbar: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
        skin: 'lightgray',
        theme : 'modern',
        language: 'pt_BR',
        language_url : '/static/vendor/tinymce/langs/pt_BR.js',
    })

})(window.angular);

(function(angular){
    'use strict';

    angular.module('messages', [
        'messages.controllers',
        'messages.services',
        'discussion.services',
        'django',
        'timtec-models',
        'ui.bootstrap',
        'ui.tinymce',
        'checklist-model',
        'truncate',
        'ngRoute',
        'ngFileUpload',
        'header',
    ]);
})(angular);

(function(angular){
    'use strict';

    var app = angular.module('dashboard', [
        'django',
        'core.services',
        'discussion.services',
        'discussion.directives',
        'dashboard.controllers',
        'header',
        'messages',
        'cards.services',
        'filters.htmlentities',
        'ngFileUpload',
        'ngRoute',
        'ngSanitize',
        'ui.bootstrap',
        'ui.select',
        'ui.tinymce',
    ]);
})(angular);

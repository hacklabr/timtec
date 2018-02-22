(function(angular){
    'use strict';

    var app = angular.module('dashboard', [
        'django',
        'core.services',
        'discussion.services',
        'dashboard.controllers',
        'header',
        'messages',
        'cards.controllers',
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

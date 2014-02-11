(function(angular){
    'use strict';

    angular.module('adminHeader', [
        'ngRoute',
        'django',
        'adminHeader.controllers',
        'forum',
        'timtec-models',
        'directive.alertPopup',
        'directive.contenteditable',
        'directive.fixedBar',
        'directive.markdowneditor',
        'directive.sortable',
        'filters.text',
        'ngResource'
    ]);
})(angular);

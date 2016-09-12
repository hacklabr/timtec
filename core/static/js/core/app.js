(function(angular){
    'use strict';

    angular.module('core', [
        'core.controllers',
        'core.services',
        'core.filters',
        'ngResource',
        'django',
        'twitterFilters',
        'ui.bootstrap',
        'angular-sortable-view',
        'directive.fixedBar',
        'directive.alertPopup',
        'directive.markdowneditor',
        'header',
    ]);

})(angular);

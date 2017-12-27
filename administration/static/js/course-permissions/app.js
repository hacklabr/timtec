(function(angular){
    'use strict';

    angular.module('course-permissions', [
        'course-permissions.controllers',
        'course-permissions.services',
        'ui.bootstrap',
        'ui.select',
        'django',
        'timtec-models',
        'ngRoute',
        'ngResource',
        'directive.fixedBar',
        'directive.alertPopup',
        'header',
    ]);
})(angular);

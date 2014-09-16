(function(angular){
    'use strict';

    angular.module('course-permissions', [
        'course-permissions.controllers',
        'adminHeader',
        'ui.bootstrap',
        'django',
        'timtec-models',
        'ngRoute',
        'ngResource'
    ]);
})(angular);

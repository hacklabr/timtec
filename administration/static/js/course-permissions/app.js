(function(angular){
    'use strict';

    angular.module('course-permissions', [
        'course-permissions.controllers',
        'ui.bootstrap',
        'django',
        'timtec-models',
        'ngRoute',
        'ngResource'
    ]);
})(angular);

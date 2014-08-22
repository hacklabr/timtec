(function(angular){
    'use strict';

    angular.module('course-permissions', [
        'course-permissions.controllers',
        'adminHeader',
        'django',
        'timtec-models',
        'ngRoute',
        'ngResource'
    ]);
})(angular);

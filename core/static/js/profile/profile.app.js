(function(angular){
    'use strict';

    angular.module('profile', [
        'profile.controllers',
        'profile.services',
        'timtec-models',
        'header',
        'django',
        'ngResource',
    ]);
})(angular);

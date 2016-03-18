(function(angular){
    'use strict';

    angular.module('profile', [
        'profile.controllers',
        'profile.services',
        'django',
        'ngResource'
    ]);
})(angular);

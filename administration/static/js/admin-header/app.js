(function(angular){
    'use strict';

    angular.module('adminHeader', [
        'adminHeader.controllers',
        'django',
        'timtec-models',
        'ngRoute',
        'ngResource'
    ]);
})(angular);

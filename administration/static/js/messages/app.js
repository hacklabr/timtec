(function(angular){
    'use strict';

    angular.module('messages', [
        'messages.controllers',
        'django',
        'timtec-models',
        'ngRoute',
    ]);
})(angular);

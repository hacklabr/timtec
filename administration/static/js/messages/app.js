(function(angular){
    'use strict';

    angular.module('messages', [
        'messages.controllers',
        'messages.services',
        'adminHeader',
        'django',
        'timtec-models',
        'ui.bootstrap',
        'markdown',
        'truncate',
        'ngRoute',
    ]);
})(angular);

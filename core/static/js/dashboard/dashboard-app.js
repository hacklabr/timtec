(function(angular){
    'use strict';

    var app = angular.module('dashboard', [
        'dashboard.controllers',
        'django',
        'core.services',
        'header',
        'messages',
    ]);
})(angular);

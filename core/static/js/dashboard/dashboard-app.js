(function(angular){
    'use strict';

    var app = angular.module('dashboard', [
        'django',
        'core.services',
        'dashboard.controllers',
        'header',
    ]);
})(angular);

(function(angular){
    'use strict';

    var app = angular.module('dashboard', [
        'django',
        'core.services',
        'discussion',
        'dashboard.controllers',
        'header',
    ]);
})(angular);

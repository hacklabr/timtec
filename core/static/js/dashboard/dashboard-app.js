(function(angular){
    'use strict';

    var app = angular.module('dashboard', [
        'django',
        'core.services',
        'discussion.services',
        'dashboard.controllers',
        'header',
    ]);
})(angular);

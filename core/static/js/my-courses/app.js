(function(angular){
    'use strict';

    var app = angular.module('my-courses', [
        'django',
        'timtec-models',
        'core.services',
        'directive.file',
        'ui.bootstrap',
        'truncate',
        'ngRoute',
        'ngResource',
        'header'
    ]);
})(angular);

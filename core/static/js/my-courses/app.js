(function(angular){
    'use strict';

    var app = angular.module('my-courses', [
        'django',
        'timtec-models',
        'directive.file',
        'ui.bootstrap',
        'ui.bootstrap.datetimepicker',
        'truncate',
        'ngRoute',
        'ngResource'
    ]);
})(angular);

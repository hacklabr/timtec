(function(angular){
    'use strict';

    var app = angular.module('courses', [
        'ngResource',
        'timtec-models',
        'core.services',
        'directive.fixedBar',
        'django',
        'ui.bootstrap',
        'directive.file',
        'header',
    ]);

})(window.angular);

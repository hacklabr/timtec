(function(angular){
    'use strict';

    angular.module('users-admin', [
        'users-admin.controllers',
        'users-admin.services',
        'ui.bootstrap',
        'django',
        //'timtec-models',
        'directive.fixedBar',
        'header',
        'directive.alertPopup'
    ]);
})(angular);

(function(angular){
    'use strict';

    angular.module('users-admin', [
        'users-admin.controllers',
        'users-admin.services',
        'ui.bootstrap',
        'django',
        //'timtec-models',
        'directive.fixedBar',
        'directive.alertPopup'
    ]);
})(angular);

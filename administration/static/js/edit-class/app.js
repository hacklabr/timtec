(function(angular){
    'use strict';

    angular.module('edit_class', [
        'edit_class.controllers',
        'djangular',
        'directive.waiting-screen',
        'directive.alertPopup',
        'directive.fixedBar',
        'ngSanitize',
        'core.services',
        'ui.bootstrap',
        'ui.select',
        'header',
    ]);
})(angular);

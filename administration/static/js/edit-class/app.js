(function(angular){
    'use strict';

    angular.module('edit_class', [
        'edit_class.controllers',
        'django',
        'directive.waiting-screen',
        'directive.alertPopup',
        'directive.fixedBar',
        'ngSanitize',
        'timtec-models',
        'ui.bootstrap',
        'ui.select',
        'header',
    ]);
})(angular);

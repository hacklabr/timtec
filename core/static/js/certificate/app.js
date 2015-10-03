(function(angular){
    'use strict';

    angular.module('certification', [
        'certification.controllers',
        'certification.services',
        'django',
        'timtec-models',
        'ui.bootstrap',
        'ui.bootstrap.datetimepicker',
        'truncate',
        'checklist-model',
        'ngRoute',
    ]);
})(angular);

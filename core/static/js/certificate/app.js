(function(angular){
    'use strict';

    angular.module('certification', [
        'certification.controllers',
        'certification.services',
        'django',
        'timtec-models',
        'directive.file',
        'directive.previewImage',
        'directive.alertPopup',
        'ui.bootstrap',
        'ui.bootstrap.datetimepicker',
        'truncate',
        'checklist-model',
        'ngRoute',
    ]);
})(angular);

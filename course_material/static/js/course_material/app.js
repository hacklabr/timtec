(function (angular) {
    'use strict';

    angular.module('courseMaterial', [
        'courseMaterial.controllers',
        'courseMaterial.services',
        'courseMaterial.directives',
        'courseMaterial.filters',
        'django',
        'directive.markdowneditor',
        'directive.alertPopup',
        'directive.fixedBar'
    ]);

})(angular);

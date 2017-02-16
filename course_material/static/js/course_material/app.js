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
        'header',
        'directive.fixedBar',
        'ui.tinymce',
        'ngFileUpload',
        'discussion.services',
    ]);

})(angular);

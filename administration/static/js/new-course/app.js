(function(angular){
    'use strict';

    angular.module('new-course', [
        'new-course.directives',
        'django',
        'timtec-models',
        'core.services',
        'directive.alertPopup',
        'directive.contenteditable',
        'directive.fixedBar',
        'directive.markdowneditor',
        'directive.sortable',
        'filters.text',
        'ngResource',
        'youtube',
        'markdown',
        'ui.bootstrap',
        'header',
    ]);
})(window.angular);

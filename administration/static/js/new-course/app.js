(function(angular){
    'use strict';

    angular.module('new-course', [
        'new-course.directives',
        'django',
        'timtec-models',
        'directive.alertPopup',
        'directive.contenteditable',
        'directive.fixedBar',
        'directive.markdowneditor',
        'directive.sortable',
        'filters.text',
        'ngResource',
        'youtube',
        'markdown',
        'ui.bootstrap'
    ]);
})(window.angular);

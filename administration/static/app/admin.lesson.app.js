(function(angular){
    'use strict';

    angular.module('admin.lesson', [
        'admin.lesson.controllers',
        'new-course.directives',
        'django',
        'directive.waiting-screen',
        'directive.alertPopup',
        'directive.contenteditable',
        'directive.codemirror',
        'core.services',
        'directive.fixedBar',
        'directive.markdowneditor',
        // 'directive.sortable',
        // 'filters.text',
        'youtube',
        // 'header',
        'ui.bootstrap'
    ]);
})(window.angular);

(function(angular){
    'use strict';

    angular.module('admin.lesson', [
        'admin.lesson.controllers',
        'admin.lesson.services',
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
        'header',
        'ui.bootstrap',
        'discussion.services',
        'discussion.directives',
        'ngFileUpload',
        'ui.tinymce',
    ]);
})(window.angular);

(function(angular){
    'use strict';

    angular.module('edit-lesson', [
        'django',
        'directive.alertPopup',
        'directive.contenteditable',
        'timtec-models',
        'directive.fixedBar',
        // 'directive.markdowneditor',
        // 'directive.sortable',
        // 'filters.text',
        'youtube'
    ]);
})(window.angular);

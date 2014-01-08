(function(angular){
    'use strict';

    angular.module('new-course', [
        'django',
        'directive.alertPopup',
        'directive.contenteditable',
        'directive.fixedBar',
        'directive.markdowneditor',
        'directive.sortable',
        'filters.text',
        'ngResource',
        'youtube'
    ]);
})(window.angular);

(function(angular){
    'use strict';

    angular.module('new-course', [
        'django',
        'timtec-models',
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

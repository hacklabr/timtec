(function(angular){
    'use strict';

    var app = angular.module('new-course', [
        'django',
        'directive.contenteditable',
        'directive.markdowneditor',
        'directive.fixedBar',
        'directive.sortable',
        'filters.text',
        'ngResource',
        'youtube'
    ]);
})(window.angular);

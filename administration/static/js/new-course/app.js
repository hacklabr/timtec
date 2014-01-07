(function(angular){
    'use strict';

    var app = angular.module('new-course', [
        'django',
        'directive.contenteditable',
        'directive.markdowneditor',
        'directive.fixedBar',
        'filters.text',
        'ngResource',
        'youtube'
    ]);
})(window.angular);

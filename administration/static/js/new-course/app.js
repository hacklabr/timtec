(function(angular){
    'use strict';

    var app = angular.module('new-course', [
        'directive.contenteditable',
        'directive.markdowneditor',
        'ngResource',
        'youtube'
    ]);

    app.config(['$httpProvider',
        function ($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ]);
})(window.angular);
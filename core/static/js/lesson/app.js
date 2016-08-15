(function(angular){
    'use strict';

    var app = angular.module('lesson', [
        'lesson.controllers',
        'lesson.services',
        'activities',
        'directive.markdowneditor',
        'directive.codemirror',
        'ngRoute',
        'ngResource',
        'youtube',
        'django',
//        'forum',
        'notes',
        'directives.layout',
        'header',
        'markdown',
        'discussion.controllers',
        'discussion.services',
        'ui.tinymce',
        'ui.bootstrap',
        'ngFileUpload',
    ]);

    app.config(['$resourceProvider', function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = true;
    }]);

})(angular);

(function(angular){
    'use strict';

    angular.module('lesson', [
        'lesson.controllers',
        'lesson.services',
        'activities',
        'directive.markdowneditor',
        'directive.codemirror',
        'ngRoute',
        'ngResource',
        'youtube',
        'django',
        'forum',
        'notes',
        'directives.layout',
    ]);

})(angular);

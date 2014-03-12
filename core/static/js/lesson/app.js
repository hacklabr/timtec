(function(angular){
    'use strict';

    angular.module('lesson', [
        'lesson.controllers',
        'lesson.services',
        'lesson.directives',
        'activities',
        'directive.markdowneditor',
        'directive.codemirror',
        'ngRoute',
        'ngResource',
        'youtube',
        'django',
        'forum',
        'notes'
    ]);

})(angular);

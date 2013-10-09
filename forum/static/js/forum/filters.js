'use strict';

/* Filters */

angular.module('forum.filters', ["ngSanitize"]).
    filter('markdown', ['$window', function($window) {
        return function(text) {
            return Markdown.getSanitizingConverter().makeHtml(text);
        };
    }]);

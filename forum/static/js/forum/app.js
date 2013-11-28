
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('forum', ['forum.services', 'forum.controllers', 'forum.filters', 'forum.directives', 'truncate']).
        config(['$routeProvider', function($routeProvider) {
        }]).
        config(function($httpProvider, $sceDelegateProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $sceDelegateProvider.resourceUrlWhitelist([
                'self',
                window.STATIC_URL + '**'])
        });
})(angular);

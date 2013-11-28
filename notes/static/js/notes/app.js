
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('notes', ['notes.services', 'notes.controllers', 'notes.directives', 'notes.filters']).
        config(function($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        });
})(angular);
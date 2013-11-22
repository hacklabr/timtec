
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('courseMaterial', ['courseMaterial.services', 'courseMaterial.controllers', 'courseMaterial.directives', 'courseMaterial.filters']).
        config(function($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        });
})(angular);
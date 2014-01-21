
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('notes', ['django', 'notes.services', 'notes.controllers', 'notes.directives', 'notes.filters']);
})(angular);

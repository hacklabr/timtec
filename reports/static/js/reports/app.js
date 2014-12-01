
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('reports', [
        'reports.controllers',
        'reports.services',
        'adminHeader',
        'timtec-models',
        'ui.bootstrap']);
})(angular);

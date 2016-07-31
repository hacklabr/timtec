
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('notes', [
        'notes.controllers',
        'notes.services',
        'django',
        'header',
        'gettext',
    ]);
})(angular);

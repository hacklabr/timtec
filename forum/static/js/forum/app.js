
(function (angular) {
    'use strict';

    // Declare app level module which depends on filters, and services
    angular.module('forum', ['django', 'forum.services', 'forum.controllers', 'forum.filters', 'forum.directives', 'truncate', 'ui.bootstrap', 'timtec-models', 'header']);
})(angular);

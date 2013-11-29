
(function (angular) {
    'use strict';
    /* Services */
    angular.module('notes.services', ['ngResource']).
        factory('Note', function($resource){
            return $resource('/api/note/', {}, {
                update: {method: 'PUT'},
            });
        });
})(angular);


(function (angular) {
    'use strict';
    /* Services */
    angular.module('notes.services', ['ngResource']).
        factory('Note', function($resource){
            return $resource('/api/note/:note_id', {}, {
                update: {method: 'PUT'},
                get: {method: 'GET', isArray: true}
            });
        }).
        factory('UserNotes', function($resource){
            return $resource('/api/lessons_notes/', {}, {
            });
        });
})(angular);

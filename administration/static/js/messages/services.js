
(function (angular) {
    'use strict';

    angular.module('messages.services', ['ngRoute', 'ngResource']).
        factory('Message', function($resource){
            return $resource('/api/professor_message/:messageId', {}, {
                update: {method: 'PUT'}
            });
        }).
        factory('User', function($resource){
            return $resource('/api/user/:userId', {}, {
            });
        }).
        factory('Student', function($resource){
            return $resource('/api/course_student/', {}, {
            });
        })
        ;
})(angular);

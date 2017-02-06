
(function (angular) {
    'use strict';

    var module = angular.module('messages.services', ['ngRoute', 'ngResource']);
    module.factory('Message', function($resource){
            return $resource('/api/professor_message/:messageId', {}, {
                update: {method: 'PUT'}
            });
    });

    module.factory('MessageGlobal', function($resource){
            return $resource('/api/professor_message_global/:messageId', {}, {
                update: {method: 'PUT'}
            });
    });

    module.factory('MessageRead', function($resource){
            return $resource('/api/professor_message_read/:message', {}, {
            });
    });

    module.factory('User', function($resource){
            return $resource('/api/user/:userId', {}, {
            });
    });

    module.factory('Group', function($resource){
            return $resource('/api/group/:groupId', {}, {
            });
    });

    module.factory('Student', function($resource){
            return $resource('/api/course_student/', {}, {});
    });
})(angular);

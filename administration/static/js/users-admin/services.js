
(function (angular) {
    'use strict';

    var module = angular.module('users-admin.services', ['ngResource']);

    module.factory('UserAdmin', function($resource){
        return $resource('/api/user_admin/:user_id', {}, {
            update: {method: 'PUT'}
        });
    });
})(angular);

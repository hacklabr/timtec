
(function (angular) {
    'use strict';

    var module = angular.module('users-admin.services', ['ngResource']);

    module.factory('UserAdmin', function($resource){
        return $resource('/api/user_admin/:user_id', {}, {
            update: {method: 'PUT'}
        });
    });

    module.factory('GroupAdmin', function($resource){
        return $resource('/api/group_admin/:id', {}, {
            update: {method: 'PUT'}
        });
    });

    module.factory('Contracts', ['$resource', function($resource){
        return $resource('/paralapraca/api/contract/:id',
            {'id': '@id'});
    }]);

})(angular);

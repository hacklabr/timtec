(function (angular) {
    'use strict';
    var module = angular.module('profile-admin.services', ['ngResource']);

    module.factory('UserProfile', function($resource){
        return $resource('/api/profile/:userId', {}, {
        });
    });

})(angular);

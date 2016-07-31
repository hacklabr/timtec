(function (angular) {
    'use strict';
    var module = angular.module('profile.services', []);

    module.factory('UserProfile', function($resource){
        return $resource('/api/profile/:userId', {}, {
        });
    });

})(angular);

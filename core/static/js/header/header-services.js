(function(angular){
    'use strict';
    var app = angular.module('header.services', ['ngResource']);
    app.factory('UserMessage', function($resource){
        return $resource('/api/user_message/', {}, {});
    });

})(window.angular);

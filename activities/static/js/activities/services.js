(function(angular){
    'use strict';

    var app = angular.module('activities.services', []);

    app.factory('resolveActivityTemplate', function(STATIC_URL) {
        return function (typeName) {
            return STATIC_URL + '/templates/activity_'+ typeName + '.html';
        };
    });

})(window.angular);


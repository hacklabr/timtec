(function(angular){
    'use strict';
    var app = angular.module('new-course');

    app.factory('course', function() {
        var course = angular.fromJson(window.localStorage.getItem('course'));

        if( !course ) {
            course = {};
        }
        var save = function () {
            window.localStorage.setItem('course', angular.toJson(course));
        };
        Object.defineProperty(course, 'save',{
            'value': save,
            'enumerable': false
        });

        return course;
    });

})(window.angular);
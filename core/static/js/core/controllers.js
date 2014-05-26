(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course', 'Twitter', function ($scope, Course, Twitter) {

        function compare_by_position(a,b) {
            if (a.home_position < b.home_position)
               return -1;
            if (a.home_position > b.home_position)
               return 1;
            return 0;
        }

        $scope.courses = Course.query({'home_published': 'True'}, function(courses) {
            courses.sort(compare_by_position);
        });
    }]);

})(angular);

(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course',
        function ($scope, Course) {
            $scope.courses = Course.query({'home_published': 'True'}, function(courses) {
                if (courses.length > 6) {
                    courses = courses.slice(0,6);
                }
            });
        }
    ]);

})(angular);

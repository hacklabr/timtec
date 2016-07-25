(function(angular){
    'use strict';
    var app = angular.module('dashboard.controllers', []);

    app.controller('DashboardCtrl', ['$scope', 'CourseStudent',
        function ($scope, CourseStudent) {
            $scope.my_courses = CourseStudent.query();
        }
    ]);

})(window.angular);
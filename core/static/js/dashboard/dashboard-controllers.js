(function(angular){
    'use strict';
    var app = angular.module('dashboard.controllers', []);

    app.controller('DashboardCtrl', ['$scope', 'CourseStudent', 'Topic',
        function ($scope, CourseStudent, Topic) {
            $scope.my_courses = CourseStudent.query();
            $scope.latest_topics = Topic.query({limit: 12, ordering: 'updated_at'})
        }
    ]);

})(window.angular);
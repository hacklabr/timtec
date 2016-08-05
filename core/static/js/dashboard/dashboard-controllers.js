(function(angular){
    'use strict';
    var app = angular.module('dashboard.controllers', []);

    app.controller('DashboardCtrl', ['$scope', 'CourseStudent', 'Topic',
        function ($scope, CourseStudent, Topic) {
            CourseStudent.query({}, function(my_courses){
                if (my_courses.length > 2) {
                    $scope.my_courses = my_courses.slice(0, 2);
                } else {
                    $scope.my_courses = my_courses;
                }
            });
            $scope.latest_topics = Topic.query({limit: 8, ordering: '-last_activity_at'})
        }
    ]);

})(window.angular);
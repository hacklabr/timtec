(function(angular){
    'use strict';
    var app = angular.module('dashboard.controllers', []);

    app.controller('DashboardCtrl', ['$scope', 'Course', 'CourseStudent', 'Topic', 'Cards',
        function ($scope, Course, CourseStudent, Topic, Cards) {

            function compare_by_course_student(a,b) {
                if (a.course_student === undefined) {
                    return 1;
                } else  {
                    if (b.course_student !== undefined) {
                        if (b.course_student.last_activity < a.course_student.last_activity)
                            return -1;
                        else
                            return 1;
                    } else {
                        return -1;
                    }
                }
                return 0;
            }

            Course.query({'public_courses': 'True'}, function (courses) {
                $scope.courses = courses;
                CourseStudent.query({}, function (course_students){
                    $scope.course_students = course_students
                    angular.forEach($scope.courses, function(course) {
                        angular.forEach($scope.course_students, function(course_student) {
                            if (course.id === course_student.course.id) {
                                course.course_student = course_student;
                            }
                        });
                    });
                    $scope.courses.sort(compare_by_course_student);
                    $scope.courses = courses.slice(0, 2);
                });
            });
            $scope.latest_topics = Topic.query({limit: 8, ordering: '-last_activity_at'})

            Cards.get({
                    is_certified: 2,
                    limit: 3
                }, function(data){
                    $scope.cards = data.results;
                });

            $scope.card_image = function(card) {
                if (card.image_gallery.length > 0)
                    return card.image_gallery[0].image;
                return '/static/img/card-default.png';
            };
        }
    ]);

})(window.angular);


(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('reports.controllers', []).
        controller('ReportsCtrl', ['$scope', '$location', '$sce', '$window', 'CourseUserReport', 'LessonsUserProgress', 'Class', 'CourseStats', 'CourseProfessor',
            function ($scope, $location, $sce, $window, CourseUserReport, LessonsUserProgress, Class, CourseStats, CourseProfessor) {
                $scope.course_id = parseInt($window.course_id, 10);
                var current_user_id = parseInt($window.user_id, 10);

                $scope.course_stats = CourseStats.get({courseId: $scope.course_id});
                $scope.users_reports = CourseUserReport.query({course: $scope.course_id}, function(data) {
		    for (var i=0; i<data.length; i++) {
			if (!data[i].name)
			    data[i].name = data[i].username;
		    }
		    return data;
		});
		$scope.ordering = 'name';
		$scope.reverse = false;

                $scope.my_classes = [];
                $scope.others_classes = [];
                $scope.filters = {
                    textsearch: '',
                    check : function(student){
			var f = $scope.filters;
			var search = f.textsearch.toLowerCase();
			var targets = [
			    student.name,
			    student.username,
			    student.email,
			];

			for (var i=0; i<targets.length; i++) {
			    if (targets[i].toLowerCase().match(search)) {
				return true;
			    }
			}

			return false;
		    }
		};

                CourseProfessor.query({course: $scope.course_id, user: current_user_id}, function(course_professor){
                    var current_user = course_professor[0];
                    var current_user_role = '';
                    // If current_user is undefined, he is not course professor, but may be admin
                    if (current_user === undefined) {
                        if ($window.is_admin)
                            // if user is admin, set role to coordinator, higher role in course.
                            current_user_role = 'coordinator';
                    } else {
                        current_user_role = current_user.role;
                    }

                    $scope.classes = Class.query({course: $scope.course_id}, function(classes){
                        if (current_user_role == 'assistant') {
                            $scope.my_classes = classes;
                            $scope.filters.selected_class = 'my_classes';
                        } else if (current_user_role == 'coordinator') {
                            $scope.filters.selected_class = 'all';
                            classes.forEach(function(klass) {
                                // if current user is undefined, he is not course professor, so he don't have any class
                                // in this course.
                                if (current_user !== undefined && klass.assistant == current_user.user) {
                                    $scope.my_classes.unshift(klass);
                                } else {
                                    $scope.others_classes.unshift(klass);
                                }
                            });
                        }
                    });
                    $scope.current_user_role =  current_user_role;
                });

                $scope.show_user_progress_details = function(user) {
                    if (user.lessons_stats === undefined) {
                        user.lessons_stats = LessonsUserProgress.get({courseId: $scope.course_id, user: user.user_id});
                    }
                };

                $scope.filter_stats = function(){
                    if ($scope.filters.selected_class == 'all') {
                        $scope.course_stats = CourseStats.get({courseId: $scope.course_id}, function (course_stats){});
                        $scope.users_reports = CourseUserReport.query({course: $scope.course_id}, function (users_reports){});
                    } else if ($scope.filters.selected_class == 'my_classes') {
                        $scope.users_reports = CourseUserReport.query({course: $scope.course_id, classes: $scope.my_classes.map(function(x) {return x.id; })});
                        $scope.course_stats = CourseStats.get({courseId: $scope.course_id, classes: $scope.my_classes.map(function(x) {return x.id; })});
                    } else if ($scope.filters.selected_class == 'others_classes') {
                        $scope.users_reports = CourseUserReport.query({course: $scope.course_id, classes: $scope.others_classes.map(function(x) {return x.id; })});
                        $scope.course_stats = CourseStats.get({courseId: $scope.course_id, classes: $scope.others_classes.map(function(x) {return x.id; })});
                    } else {
                        $scope.users_reports = CourseUserReport.query({course: $scope.course_id, classes: $scope.filters.selected_class});
                        $scope.course_stats = CourseStats.get({courseId: $scope.course_id, classes: $scope.filters.selected_class});
                    }
                };
        }]);
})(angular);

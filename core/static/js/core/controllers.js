(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course', 'CarouselCourse', 'Twitter', 'FlatPage', function ($scope, Course, CarouselCourse, Twitter, FlatPage) {

        var success_save_msg = 'Alterações salvas com sucesso.';

        function compare_by_position(a,b) {
            if (a.home_position < b.home_position)
               return -1;
            if (a.home_position > b.home_position)
               return 1;
            return 0;
        }

        // Fetch home courses
        $scope.home_courses = Course.query({'home_published': 'True'}, function(home_courses) {
            home_courses.sort(compare_by_position);
            $scope.home_courses_bkp = angular.copy(home_courses);
            return home_courses;
        });

        $scope.home_bottom_intro = new FlatPage();
        $scope.home_bottom_intro.url = '/home/bottom/intro/';
        $scope.home_bottom_intro.title = '';

        $scope.home_bottom_center = new FlatPage();
        $scope.home_bottom_center.url = '/home/bottom/center/';
        $scope.home_bottom_center.title = '';

        $scope.home_bottom_left = new FlatPage();
        $scope.home_bottom_left.url = '/home/bottom/left/';
        $scope.home_bottom_left.title = '';

        $scope.home_bottom_right = new FlatPage();
        $scope.home_bottom_right.url = '/home/bottom/right/';
        $scope.home_bottom_right.title = '';

        // Here starts the Admin
        $scope.bottom_home_flatpages = FlatPage.query({url_prefix: '/home/bottom/'}, function(bottom_text_flatpages){
            angular.forEach(bottom_text_flatpages, function(flatpage) {
                if (flatpage.url == '/home/bottom/intro/'){
                    $scope.home_bottom_intro = flatpage;
                } else if (flatpage.url == '/home/bottom/center/'){
                    $scope.home_bottom_center = flatpage;
                } else if (flatpage.url == '/home/bottom/left/'){
                    $scope.home_bottom_left = flatpage;
                } else if (flatpage.url == '/home/bottom/right/'){
                    $scope.home_bottom_right = flatpage;
                }
            });
        });

        $scope.all_courses = Course.query({'public_courses': 'True'}, function (all_courses) {
            $scope.all_courses_bkp = angular.copy(all_courses);
        });

        $scope.start_changing_home_cousers = function () {
            $scope.home_courses_changed = angular.copy($scope.home_courses);
            $scope.all_courses_before_changes = angular.copy($scope.all_courses);
        };

        var last_position = 100;
        $scope.selectCourse = function(course) {
            // if the course is not published in home, insert it in home courses and set its positions to last.
            // If the course is in home_published, it will be saved to set the new home_position. If it isn't,
            // the 'toBeSaved is set true to save it.
            if (!course.home_published) {
                course.home_position = last_position;
                last_position +=1;
                $scope.home_courses_changed.push(course);
            } else {
                for (var i = 0; i < $scope.home_courses_changed.length; i++) {
                    if (course.slug == $scope.home_courses_changed[i].slug) {
                        $scope.home_courses_changed.splice(i, 1);
                        break;
                    }
                }
                course.toBeSaved = true;
            }
            course.home_published = !course.home_published;
        };

        $scope.cancel_courses_selection = function(course) {
        //    $scope.home_courses = $scope.home_courses_bkp;
            $scope.all_courses = angular.copy($scope.all_courses_before_changes);
        };

        $scope.apply_courses_selection = function() {

            $scope.home_courses = angular.copy($scope.home_courses_changed);
            //$scope.all_courses = angular.copy($scope.all_courses_changed);
            $scope.order_changed = true;

            //$scope.alert.success(success_save_msg);
        };

        // controls if home order has changed
        $scope.order_changed = false;

        $scope.set_order_changed = function() {
            $scope.order_changed = true;
        };

        $scope.save_home = function() {
            if ($scope.order_changed) {
                $scope.home_courses.forEach(function(course, i){
                    course.home_position = i;
                    course.$update({courseId: course.id});
                });
            }
            $scope.order_changed = false;

            angular.forEach($scope.all_courses, function(course) {
                if (course.toBeSaved && !course.home_published) {
                    course.$update({courseId: course.id});
                }
            });
            $scope.alert.success(success_save_msg);
        };

        $scope.cancel_home_changes = function() {
            $scope.home_courses = angular.copy($scope.home_courses_bkp);
            $scope.all_courses = angular.copy($scope.all_courses_bkp);
            $scope.alert.success('Alterações nos cursos da home canceladas.');
        };

        $scope.save_home_text = function(flatpage) {
            if (flatpage.id) {
                flatpage.$update({flatpageId: flatpage.id});
            } else {
                flatpage.$save();
            }
            $scope.alert.success(success_save_msg);
        };

        // Upcoming course and twitter, only for timtec theme
        $scope.upcoming_courses = CarouselCourse.query({'home_published': 'False'}, function(upcoming_courses) {
            $scope.upcoming_courses_rows_3 = [];
            if (upcoming_courses.length > 3) {
                for (var i = 0; i < upcoming_courses.length; i++) {
                    var row = [];
                    row[0] = $scope.upcoming_courses[i];

                    if (upcoming_courses.length - i > 1) {
                        // normal case
                        row[1] = $scope.upcoming_courses[i + 1];
                        if (upcoming_courses.length - i > 2)
                            row[2] = $scope.upcoming_courses[i + 2];
                        else
                            row[2] = $scope.upcoming_courses[upcoming_courses.length - i - 2];
                    } else {
                        row[1] = $scope.upcoming_courses[upcoming_courses.length - i - 1];
                        row[2] = $scope.upcoming_courses[upcoming_courses.length - i];
                    }
                    $scope.upcoming_courses_rows_3.push(row);
                }
            }
            return upcoming_courses;
        });

        $scope.twits = Twitter.query({});
    }]);

})(angular);


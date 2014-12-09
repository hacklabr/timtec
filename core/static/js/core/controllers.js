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
            return home_courses.sort(compare_by_position);
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

        $scope.all_courses = Course.query({'public_courses': 'True'});

        $scope.selectCourse = function(course) {
            course.home_published = !course.home_published;
            course.toBeSaved = true;
        };

        $scope.saveCourses = function(course) {
            var home_courses = [];
            angular.forEach($scope.all_courses, function(course) {
                if (course.home_published) {
                    home_courses.push(course);
                }
                if (course.toBeSaved) {
                    course.$update({courseId: course.id});
                }
            });
            home_courses.sort(compare_by_position);
            $scope.home_courses = home_courses;
            $scope.alert.success(success_save_msg);
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
            $scope.alert.success(success_save_msg);

        };

        $scope.cancel_home_changes = function() {
            $scope.home_courses = $scope.home_courses.sort(compare_by_position);
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

            for (var i = 0; i < upcoming_courses.length; i++) {
                var row = [];
                row[0] = $scope.upcoming_courses[i];

                if (upcoming_courses.length - i > 1){
                    // normal case
                    row[1] = $scope.upcoming_courses[i+1];
                    if (upcoming_courses.length - i > 2)
                        row[2] = $scope.upcoming_courses[i+2];
                    else
                        row[2] = $scope.upcoming_courses[upcoming_courses.length - i - 2];
                } else {
                    row[1] = $scope.upcoming_courses[upcoming_courses.length - i - 1];
                    row[2] = $scope.upcoming_courses[upcoming_courses.length - i];
                }
                $scope.upcoming_courses_rows_3.push(row);
            }
        });

        $scope.twits = Twitter.query({});
    }]);

})(angular);


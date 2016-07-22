(function(angular){
    'use strict';
    var app = angular.module('dashboard.controllers', []);

    app.controller('DashboardCtrl', ['$scope', 'CourseStudent',
        function ($scope, CourseStudent) {
            $scope.my_courses = CourseStudent.query();
//            $scope.my_courses.$promise.then(function(res){
//                var rows = [],
//                    row = [],
//                    n = 0,
//                    i = 0;
//                var sorted = res.sort(function(a,b){
//                        return b.percent_progress-a.percent_progress; // ordering by percentage
//                });
//                console.log(sorted)
//                for(var i = 0; i<sorted.length;i++){ // keeping courses in pairs for layout purposes
//                    if(i == 6) {
//                        break;
//                    }
//                    if(n < 2) {
//                        row.push(sorted[i]);
//                        n++;
//                    }
//                    else {
//                        rows.push(row);
//                        row = [];
//                        n=0;
//                    }
//                };
//                $scope.courses_rows = rows;
//            });
        }
    ]);

})(window.angular);
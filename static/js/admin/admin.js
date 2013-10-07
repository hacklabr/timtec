(function(angular){
    "use strict";

    var courseSlug = /[^/]+$/.extract(location.pathname);
    var app = angular.module('admin', ['ngRoute', 'ngResource', 'ngSanitize']);

    app.directive('contenteditable', function(){
        return {
            "restrict": 'A',
            "require": '?ngModel',
            "link": function(scope, element, attrs, ngModel) {
                if(!ngModel) return;
                ngModel.$render = function(){ element.html(ngModel.$viewValue || ''); };
                element.on('blur keyup change', function() { scope.$apply(read); });
                function read() {
                    var html = element.html();
                    if( attrs.stripBr && html.match(/ *<br\/?> */) ){
                      html = "";
                    }
                    ngModel.$setViewValue(html);
                }
            }
        };
    });


    app.controller('CourseEdit',['$scope','CourseDataFactory',
        function($scope, CourseDataFactory){
            $scope.modals = ['application', 'requirement', 'abstract', 'structure', 'workload'];

            CourseDataFactory.then(function(course){
                var __course__ = angular.copy(course);
                $scope.course = course;
                $scope.reset = function(field) {
                    course[field] = angular.copy(__course__[field]);
                };
            });
        }
    ]);


    app.factory('CourseDataFactory', ['$rootScope', '$q', '$resource',
        function($rootScope, $q, $resource, $window) {
            var Course = $resource('/api/course/:courseSlug/',{'courseSlug': courseSlug});
            var deferred = $q.defer();

            Course.get(function(course){
                deferred.resolve(course);
            });
            return deferred.promise;
        }
    ]);
})(angular);
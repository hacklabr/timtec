(function(angular){
    "use strict";

    var courseSlug = /[^/]+$/.extract(location.pathname);
    var app = angular.module('admin', ['ngRoute', 'ngResource', 'ngSanitize']);

    app.config(['$httpProvider',
        function ($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ]);


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


    app.controller('CourseEdit',['$scope','CourseDataFactory', '$http',
        function($scope, CourseDataFactory, $http){
            $scope.modals = ['application', 'requirement', 'abstract', 'structure', 'workload'];

            CourseDataFactory.then(function(course){
                var __course__ = angular.copy(course);
                $scope.course = course;

                function update_backup(field){
                    __course__[field] = course[field];
                }

                $scope.reset = function(field) {
                    course[field] = angular.copy(__course__[field]);
                };

                $scope.save = function(field) {
                    var data = { };
                    data[field] = course[field];

                    $http(
                        {
                            'method': 'POST',
                            'url': '/api/course/' + courseSlug,
                            'data': data,
                            'headers': {'Content-Type': 'application/json; charset=utf-8'}
                        }
                    ).success(function(){update_backup(field);});
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
                window._c = course;
            });
            return deferred.promise;
        }
    ]);
})(angular);
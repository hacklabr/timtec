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


    app.controller('CourseEdit',['$scope','CourseData',
        function($scope, CourseData){
            $scope.modals = ['application', 'requirement', 'abstract',
                             'structure', 'workload'];

            CourseData.then(function(course){

            });
        }
    ]);


    app.factory('CourseData', ['$rootScope', '$q', '$resource',
        function($rootScope, $q, $resource, $window) {
            var Course = $resource('/api/course/:courseSlug/');
            var deferred = $q.defer();
            Course.get({'courseSlug': courseSlug}, function(course){
                $rootScope.course = course;
                deferred.resolve(course);
            });
            return deferred.promise;
        }
    ]);
})(angular);
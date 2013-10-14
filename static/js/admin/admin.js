(function(angular){
    "use strict";

    var courseSlug = /[^/]+$/.extract(location.pathname);
    var getYoutubeUrl = function(id, params){
        var localparams = {"rel":"0", "showinfo":"0", "autohide":"1", "theme":"light"};

        for(var att in params){
            localparams[att] = params[att];
        }

        var url = new URL("https://www.youtube.com/embed/"+id, localparams);
        return url.toString();
    };

    var app = angular.module('admin', ['ngRoute', 'ngResource', 'ngSanitize']);

    app.config(['$httpProvider', '$sceDelegateProvider',
        function ($httpProvider, $sceDelegateProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $sceDelegateProvider.resourceUrlWhitelist(['^.*$', 'self']);
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


    app.controller('CourseEdit',['$scope', 'LessonDataFactory', 'CourseDataFactory', '$http',
        function($scope, LessonDataFactory, CourseDataFactory, $http){
            $scope.course = {};
            $scope.modals = ['application', 'requirement', 'abstract', 'structure', 'workload'];

            $scope.show = function(){
                try{
                    return getYoutubeUrl($scope.course.intro_video.youtube_id);
                } catch(e) {
                    return 'data:text/html, <html style="background: black">';
                }
            };

            CourseDataFactory.then(function(course){
                $scope.course = course;
            });
            LessonDataFactory.then(function(lessons){
                $scope.lessons = lessons;
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

    app.factory('LessonDataFactory', ['$rootScope', '$q', '$resource',
        function($rootScope, $q, $resource, $window) {
            var Lesson = $resource('/api/lessons?course__slug=:courseSlug',
                                    {'courseSlug': courseSlug});
            var deferred = $q.defer();

            Lesson.query(function(lessons){
                deferred.resolve(lessons);
            });
            return deferred.promise;
        }
    ]);


})(angular);
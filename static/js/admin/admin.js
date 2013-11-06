(function(angular){
    "use strict";

    var courseSlug = /[^/]+$/.extract(location.pathname);
    var app = angular.module('admin', ['ngRoute', 'ngResource', 'ngSanitize', 'youtube']);

    app.config(['$httpProvider', '$sceDelegateProvider',
        function ($httpProvider, $sceDelegateProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $sceDelegateProvider.resourceUrlWhitelist([
                /^https?:\/\/(www\.)?youtube\.com\/.*/,
                'data:text/html, <html style="background: white">'
            ]);
            window.sce = $sceDelegateProvider;
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

    /**
     * Controllers
     */
    app.controller('CourseEdit',['$scope', 'CourseDataFactory', '$http', 'youtubePlayerApi',
        function($scope, CourseDataFactory, $http, youtubePlayerApi){
            $scope.course = {};
            $scope.video = {
                'name': null,
                'youtube_id': null,
                'save': function() {
                    if(this.youtube_id_temp) {
                        this.youtube_id = this.youtube_id_temp;
                        $scope.course.intro_video = this;
                        $scope.course.$save().then((function(){
                            youtubePlayerApi.player.cueVideoById(this.youtube_id);
                        }).bind(this));
                    }
                },
                'reset': function() {
                    this.youtube_id = $scope.course.intro_video.youtube_id;
                }
            };

            var fields = ['application', 'requirement', 'abstract', 'structure', 'workload'];

            var build_data_for_modals = function(field){
                return {
                    'status': '',
                    'window': field,
                    'data': angular.copy($scope.course[field]),
                    'reset': function(){
                        this.data = angular.copy($scope.course[field]);
                    },
                    'save': function(){
                        var self = this;
                        var old = angular.copy($scope.course[field]);
                        $scope.course[field] = self.data;
                        $scope.course.$save()
                            .then(function(){
                                self.status = 'saved';
                            }).catch(function(){
                                self.status = 'error';
                                $scope.course[field] = old;
                            });
                    }
                };
            };

            CourseDataFactory.then(function(course){
                $scope.course = angular.copy(course);
                $scope.modals = fields.map(build_data_for_modals);
                if($scope.course.intro_video){
                    $scope.video.name = $scope.course.intro_video.name;
                    $scope.video.youtube_id = $scope.course.intro_video.youtube_id;

                    youtubePlayerApi.events = {
                        'onReady': function(player){
                            player.target.cueVideoById($scope.video.youtube_id);
                        }
                    };
                }
                youtubePlayerApi.loadPlayer();
                // reindex $scope.modals
                fields.forEach(function(e,i){$scope.modals[e]=$scope.modals[i];});
            });
        }
    ]);

    app.controller('LessonList',['$scope', '$rootScope', 'LessonListFactory', '$http',
        function($scope, $rootScope, LessonListFactory, $http){

            $scope.select = function (lesson) {
                $rootScope.selectedLesson = lesson;
                return lesson;
            };
            $scope.countActivities = function(l) {
                if( l.units ) {
                    return l.units.reduce(function(p,s){return p + (s.activity ? 1 : 0); }, 0);
                }
                return 0;
            };
            $scope.countVideos = function(l) {
                if( l.units ) {
                    return l.units.reduce(function(p,s){return p + (s.video ? 1 : 0); }, 0);
                }
                return 0;
            };

            LessonListFactory.then(function(lessons){
                $scope.lessons = lessons;
            });
        }
    ]);

    app.controller('LessonEdit',['$scope', '$rootScope', 'LessonListFactory', '$http',
        function($scope, $rootScope, LessonListFactory, $http){
            $scope.active = 'content';

            var selectedUnitIndex = 0;
            $scope.selectUnit = function(index) {
                selectedUnitIndex = index;
            };
            $scope.deleteUnit = function(index) {
                $rootScope.selectedLesson.units.splice(index, 1);
            };
            $scope.addUnit = function() {
                var pos = $rootScope.selectedLesson.units.length;
                $rootScope.selectedLesson.units.push({
                    "activity": null,
                    "id": null,
                    "position": pos,
                    "title": "",
                    "video": {
                        "id": null,
                        "name":"",
                        "youtube_id":"",
                    }
                });
            };
            $scope.selectedUnit = function() {
                if($rootScope.selectedLesson)
                    return $rootScope.selectedLesson.units[selectedUnitIndex];
            };
            $scope.activity = function() {
                if($scope.selectedUnit() && $scope.selectedUnit().activity)
                    return $scope.selectedUnit().activity;
            };
            $scope.typeIs = function(type) {
                return $scope.activity() && $scope.activity().type === type;
            };
            $scope.changeTypeTo = function(type) {
                if(!$scope.activity()) {
                    $scope.selectedUnit().activity = {
                        "type": type,
                        "data": {"question":""}
                    };
                } else {
                    $scope.activity().type = type;
                }
            };
            $scope.addAlternative = function(){
                if(!$scope.activity().data.alternatives) {
                    $scope.activity().data.alternatives = [""];
                    $scope.activity().expected = [false];
                } else {
                    $scope.activity().data.alternatives.push("");
                    $scope.activity().expected.push(false);
                }
            }
            LessonListFactory.then(function(lessons){
                $scope.lessons = lessons;
            });
        }
    ]);


    /**
     * Factories
     */
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

    app.factory('LessonListFactory', ['$rootScope', '$q', '$resource',
        function($rootScope, $q, $resource, $window) {
            var resourceConfig = {
                'get':  {
                    'method':'GET',
                    'params':{'course__slug': courseSlug}
                },
                'query':{
                    'method':'GET',
                    'params':{'course__slug': courseSlug},
                    'isArray': true
                },
                'update':{
                    'method': 'PUT'
                }
            };
            var LessonList = $resource('/api/lessons/:id', {'id':'@id'}, resourceConfig);
            var deferred = $q.defer();

            LessonList.query(function(lessons){
                deferred.resolve(lessons);
            });
            return deferred.promise;
        }
    ]);


})(angular);
(function(angular){
    'use strict';

    var courseSlug = /[^/]+$/.extract(location.pathname);
    var app = angular.module('admin', ['ngRoute', 'ngResource', 'ngSanitize', 'youtube',
                                       'directive.markdowneditor', 'directive.contenteditable']);

    app.config(['$httpProvider', '$sceDelegateProvider',
        function ($httpProvider, $sceDelegateProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $sceDelegateProvider.resourceUrlWhitelist([
                /^https?:\/\/(www\.)?youtube\.com\/.*/,
                'data:text/html, <html style="background: white">',
                'self',
                window.STATIC_URL + '**'
            ]);
        }
    ]);


    /**
     * Controllers
     */
    app.controller('CourseEdit',['$scope', 'CourseDataFactory', '$http', 'youtubePlayerApi',
        function($scope, CourseDataFactory, $http, youtubePlayerApi){
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

            $scope.saveCourse = function(){
                $scope.course.$save();
            };

            CourseDataFactory.then(function(course){
                $scope.course = course;
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
            });
        }
    ]);

    app.controller('LessonList',['$scope', '$rootScope', 'LessonListFactory', 'Lesson',
        function($scope, $rootScope, LessonListFactory, Lesson){

            $scope.newLesson = function() {
                var newLesson = new Lesson({'units': []});
                newLesson.position = $scope.lessons.length;
                $scope.lessons.push(newLesson);
                $rootScope.selectedLesson = newLesson;
            };

            $scope.select = function (lesson) {
                $rootScope.selectedLesson = lesson;
                return lesson;
            };
            $scope.countActivities = function(l) {
                if( !l.units ){
                    l.units = [];
                    return 0;
                }
                return l.units.reduce(function(p,s){return p + (s.activity ? 1 : 0); }, 0);
            };
            $scope.countVideos = function(l) {
                if( !l.units ) {
                    l.units = [];
                    return 0;
                }
                return l.units.reduce(function(p,s){return p + (s.video ? 1 : 0); }, 0);
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
                if($rootScope.selectedLesson && 'units' in $rootScope.selectedLesson)
                    if($rootScope.selectedLesson.units.length > 0){
                        return $rootScope.selectedLesson.units[selectedUnitIndex];
                    } else {
                        return {};
                    }
            };
            $scope.activity = function() {
                if($scope.selectedUnit() && $scope.selectedUnit().activity){
                    return $scope.selectedUnit().activity;
                }
            };
            $scope.typeIs = function(type) {
                return $scope.activity() && $scope.activity().type === type;
            };
            $scope.changeTypeTo = function(type) {
                if(!$scope.activity()) {
                    $scope.selectedUnit().activity = {
                        "data": {"question":""}
                    };
                }
                var act = $scope.activity();
                act.type = type;
                if(['multiplechoice', 'trueorfalse'].indexOf(act.type) >= 0){
                    if(!act.expected)
                        act.expected = (act.data.alternatives || []).map(function(){ return false; });
                } else {
                    act.expected = null;
                }
            };
            $scope.addAlternative = function(){
                var act = $scope.activity();

                if(!act.data.alternatives) {
                    act.data.alternatives = [];
                }
                act.data.alternatives.push("");

                if(['multiplechoice', 'trueorfalse'].indexOf(act.type) >= 0){
                    if(!act.expected)
                        act.expected = [];
                    act.expected.push(false);
                }
            };
            $scope.saveLesson = function(){
                if('id' in $rootScope.selectedLesson){
                    $rootScope.selectedLesson.$update();
                } else {
                    $rootScope.selectedLesson.$create();
                }
            };
            LessonListFactory.then(function(lessons){
                $scope.lessons = lessons;
            });
        }
    ]);


    /**
     * Factories
     */
    app.factory('CourseDataFactory', ['$rootScope', '$q', '$resource',
        function($rootScope, $q, $resource) {
            var Course = $resource('/api/course/:courseSlug/',{'courseSlug': courseSlug});
            var deferred = $q.defer();
            var antiCache = {
                ie: (new Date()).getTime().toString(16)
            };
            Course.get(antiCache, function(course){
                deferred.resolve(course);
            });
            return deferred.promise;
        }
    ]);

    app.factory('LessonListFactory', ['$q', '$resource',
        function($q, $resource) {
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
    app.factory('Lesson',['$resource',
        function($resource){
            var resourceConfig = {
                'get':  {
                    'method':'GET',
                    'params':{'course__slug': courseSlug}
                },
                'create':{
                    'method':'POST',
                    'transformRequest': function(data, getter){
                        data.course = courseSlug;
                        return JSON.stringify(data);
                    }
                },
                'update':{
                    'method': 'PUT'
                }
            };
            return $resource('/api/lessons/:id', {'id':'@id'}, resourceConfig);
        }
    ]);
})(angular);

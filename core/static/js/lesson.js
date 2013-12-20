(function (angular) {
    "use strict";

    var ga = window.ga || function(){ };
    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube', 'django', 'forum', 'notes', 'activities', 'lesson.services']);

    app.config(['$routeProvider', '$httpProvider', '$sceDelegateProvider',
        function ($routeProvider, $httpProvider, $sceDelegateProvider) {
            $routeProvider
                .when('/:unitPos', {
                    templateUrl: STATIC_URL + '/templates/lesson_video.html',
                    controller: 'LessonVideoCtrl',
                    resolve: {
                        'lessonData': 'LessonData',
                    }
                })
                .when('/:unitPos/activity', {
                    templateUrl: STATIC_URL + '/templates/lesson_activity.html',
                    controller: 'LessonActivityCtrl',
                    resolve: {
                        'lessonData': 'LessonData',
                        'answer': function (Answer, lessonData, $q) {
                            var deferred = $q.defer();
                            function return_last (activities) {
                                return deferred.resolve(activities.pop())
                            }
                            Answer.query({'activity': unit.activity.id}).then(return_last)
                            return deferred
                        }
                    }
                })
                .otherwise({redirectTo: '/1'});
        }
    ]);

    app.controller('LessonMainCtrl', ['$scope', 'LessonData', '$location',
        function ($scope, LessonData, $location) {
            window.l = $location;
            var match = location.hash.match(/^#\/(\d+)/);
            if(match) {
                $scope.currentUnitPos = parseInt(match[1], 10);
            } else {
                $scope.currentUnitPos = 1;
            }
            var start;

            $scope.$watch('currentUnitPos', function() {
                // Changing Unit means unit starting
                if (start) {
                    var end = new Date().getTime();
                    ga('send', 'event', 'unit', 'time in unit',
                       LessonData.course + ' - ' + LessonData.name + ' - ' + $scope.currentUnitPos,
                       end - start);
                }
                ga('send', 'event', 'unit', 'start', LessonData.course + ' - ' + LessonData.name, $scope.currentUnitPos);
                start = new Date().getTime();
            });

            $scope.isSelected = function(i){
                return $scope.currentUnitPos === i;
            };
            $scope.isDone = function(unit){
                return (unit.progress || {}).complete;
            };
            $scope.select = function(i) {
                $scope.currentUnitPos = parseInt(i,10);
                $location.path('/' + $scope.currentUnitPos);
            };

        }
    ]);

    app.controller('LessonVideoCtrl', ['$scope', '$http', '$location', 'LessonData', 'youtubePlayerApi',
        function ($scope, $http, $location, LessonData, youtubePlayerApi) {
            var $main = $scope.$parent;
            var currentUnitIndex = $main.currentUnitPos - 1;
            var _pauseFlag = false;
            var start, whole;

            var onPlayerStateChange = function (event) {
                if (event.data == YT.PlayerState.PLAYING){
                        ga('send', 'event', 'videos', 'play', $scope.currentUnit.video.youtube_id);
                        //thy video plays
                        //reaffirm the pausal beast is not with us
                        _pauseFlag = false;
                        if (whole !== 'ended' && whole !== 'started') {
                            start = new Date().getTime();
                            whole = 'started';
                        }
                }
                //should the video tire out and cease
                if (event.data == YT.PlayerState.ENDED){
                    ga('send', 'event', 'videos', 'watch To end', $scope.currentUnit.video.youtube_id);
                    if (whole === 'started') {
                        var stop = new Date().getTime();
                        var delta_s = (stop - start) / 1000;
                        ga('send', 'event', 'videos', 'time tO end', $scope.currentUnit.video.youtube_id, Math.round(delta_s));
                        whole = 'ended';
                    }
                }
                //and should we tell it to halt, cease, heal.
                //confirm the pause has but one head and it flies not its flag
                //lo the pause event will spawn a many headed monster
                //with events overflowing
                if (event.data == YT.PlayerState.PAUSED && _pauseFlag === false){
                    ga('send', 'event', 'videos', 'pause', $scope.currentUnit.video.youtube_id);
                    //tell the monster it may have
                    //but one head
                    _pauseFlag = true;
                }
                //and should the monster think, before it doth play
                //after we command it to move
                if (event.data == YT.PlayerState.BUFFERING){
                    ga('send', 'event', 'videos', 'bufferIng', $scope.currentUnit.video.youtube_id);
                }
                //and should it cue
                //for why not track this as well.
                if (event.data == YT.PlayerState.CUED){
                    ga('send', 'event', 'videos', 'cueing', $scope.currentUnit.video.youtube_id);
                }

                if (event.data === YT.PlayerState.ENDED) {
                    if( $scope.currentUnit.activity ) {
                        $location.path('/' + $main.currentUnitPos + '/activity').search('autoplay', null);
                    } else {
                        if ($main.currentUnitPos + 1 <= $scope.lesson.units.length) {
                            $main.currentUnitPos++;
                            $location.path('/' + $main.currentUnitPos).search('autoplay', null);
                        }
                        $http({
                            'method': 'POST',
                            'url': '/api/updatestudentprogress/' + $scope.currentUnitId + '/',
                            'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                        }).success(function(data){
                            $scope.currentUnit.progress = {complete: data.complete};
                            if (data.complete) {
                                ga("send", "event", "unit", "unit completed");
                            }
                        });
                    }
                    $scope.$apply();
                }
            };

            LessonData.then(function (lesson) {
                $scope.currentUnit = lesson.units[(currentUnitIndex || 0)];
                $scope.currentUnitId = $scope.currentUnit.id;

                if ($scope.currentUnit.video) {
                    if ($location.search().autoplay) {
                        youtubePlayerApi.autoplay = 1;
                    } else {
                        youtubePlayerApi.autoplay = 0;
                    }
                    youtubePlayerApi.videoId = $scope.currentUnit.video.youtube_id;
                    youtubePlayerApi.events = {
                        onStateChange: onPlayerStateChange
                    };
                    youtubePlayerApi.loadPlayer();
                }
            });
        }
    ]);

    var services = angular.module('lesson.services', ['ngResource']);

    services.factory('Answer',['$resource',
        function($resource){
            return $resource('/api/answer/:id', {'id':'@id'});
        }
    ]);

    services.factory('LessonData', ['$rootScope', '$q', '$resource', '$window',
        function($rootScope, $q, $resource, $window) {
            var Lesson = $resource('/api/lessons/:lessonId/');
            var Progress = $resource('/api/student_progress?unit__lesson=:lessonId');
            var deferred = $q.defer();

            Lesson.get({'lessonId': $window.lessonId}, function (lesson) {
                $rootScope.lesson = lesson;
                deferred.resolve(lesson);
            });

            Progress.query({'lessonId': $window.lessonId}, function (progress) {
                deferred.promise.then(function (lesson) {
                    for (var i = progress.length - 1; i >= 0; i--) {
                        var p = progress[i];
                        for (var j = lesson.units.length - 1; j >= 0; j--) {
                            if (lesson.units[j].id === p.unit) {
                                lesson.units[j].progress = p;
                            }
                        }
                    }
                });
            });

            return deferred.promise;
        }
    ]);

})(angular);

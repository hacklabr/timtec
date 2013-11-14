/** TODO: initialize this in proprer way (fabio) */
function initialize_code_mirror($scope, data, expected) {
    var body = $('#empty').contents().find('body');
    var cm = CodeMirror.fromTextArea($('#texto')[0], CodeMirrorConf);
    cm.setSize("100%", "215px"); // TODO: set size in html
    cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
    cm.markText({line:4, ch:1000}, {line:7, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});
    cm.replaceRange(data, {line:4, ch:0}, {line:4, ch:100});
    setTimeout(function () {
        $('#empty').contents().find('body').html(cm.getValue());
        $('#expected_iframe').contents().find('body').html('' + expected);
    }, 800);
    cm.on('change', function (instance) {
        data = instance.getValue();
        $('#empty').contents().find('body').html(data);
        $scope.answer.given = data;
    });
}

(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube', 'forum']);

    var ACTIVITY_TEMPLATE_PATH = function(the_type){
        return STATIC_URL + '/templates/activity_'+ the_type + '.html';
    };

    app.config(['$routeProvider', '$httpProvider',
        function ($routeProvider, $httpProvider) {
            $routeProvider
                .when('/:unitPos', {
                    templateUrl: STATIC_URL + '/templates/lesson_video.html',
                    controller: 'LessonVideoCtrl'})
                .when('/:unitPos/activity', {
                    templateUrl: STATIC_URL + '/templates/lesson_activity.html',
                    controller: 'LessonActivityCtrl'})
                .otherwise({redirectTo: '/1'});

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ]);

    app.controller('LessonMainCtrl', ['$scope', 'LessonData',
        function ($scope, LessonData) {
            var match = location.hash.match(/^#\/(\d+)/);
            if(match) {
                $scope.currentUnitPos = parseInt( match[1], 10);
            } else {
                $scope.currentUnitPos = 1;
            }

            $scope.isSelected = function(i){
                return ($scope.currentUnitPos-1) === i;
            };
            $scope.isDone = function(unit){
                return (unit.progress || {}).complete;
            };
            $scope.select = function(i) {
                $scope.currentUnitPos = i+1;
            };
        }
    ]);

    app.controller('LessonActivityCtrl', ['$scope', '$location', '$routeParams', '$http', 'LessonData',
        function ($scope, $location, $routeParams, $http, LessonData) {
            var $main = $scope.$parent;

            $scope.alternatives = [];
            $scope.currentUnitIndex = $main.currentUnitPos - 1;
            $scope.answer = {'given': null};
            $scope.sendOrNextText = 'Enviar';

            $scope.nextVideo = function() {
                $main.currentUnitPos++;
                $location.path('/' + $main.currentUnitPos).search('autoplay', null);
            };
            $scope.replayVideo = function() {
                $location.path('/' + $main.currentUnitPos).search('autoplay', 1);
            };

            $scope.sendOrNext = function() {
                if ($scope.correct) {
                    $scope.nextVideo();
                } else {
                    $scope.sendAnswer();
                }
            };

            $scope.sendAnswer = function() {
                function tellResult(data) {
                    var correct = data.correct,
                        given  = data.given,
                        expected  = data.expected;

                    if(correct){
                        ga('send', 'event', 'activiTy', 'result', '', 1);
                        $scope.currentUnit.progress = {complete : true};
                        $scope.correct = true;
                        $scope.sendOrNextText = "Continuar";
                    } else {
                        ga('send', 'event', 'activiTy', 'result', '', 0);
                    }

                    $scope.isCorrect = correct;
                }

                ga('send', 'event', 'activiTy', 'submit');

                $http({
                    'method': 'POST',
                    'url': '/api/answer/' + $scope.currentUnitId,
                    'data': 'given=' + JSON.stringify($scope.answer.given),
                    'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                }).success(tellResult);
            };

            LessonData.then(function (lesson) {
                var unit = $scope.currentUnit = lesson.units[$scope.currentUnitIndex];
                $scope.currentUnitId = unit.id;
                $scope.activity_template = unit.activity.template;

                if (unit.activity.data.alternatives) {
                    $scope.alternatives = unit.activity.data.alternatives.map(
                        function(a,i) { return {'title': a }; }
                    );
                }

                if (unit.activity.type == 'multiplechoice') {
                    $scope.answer.given = $scope.alternatives.map(
                        function(a,i){ return false; }
                    );
                } else if (unit.activity.type == 'trueorfalse') {
                    $scope.answer.given = $scope.alternatives.map(
                        function(a,i){ return null; }
                    );
                } else if(unit.activity.type === 'relationship') {
                    $scope.answer.given = unit.activity.data.column1.map(
                        function(a,i){ return null; }
                    );
                } else if(unit.activity.type === 'html5') {
                    /** TODO: initialize this in proprer way (fabio) */
                    setTimeout(function () {
                        initialize_code_mirror($scope, unit.activity.data.data, unit.activity.expected.expected_answer);
                    }, 100);
                }

            });
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
                        if ($main.currentUnitPos + 1 < $scope.lesson.units.length) {
                            $main.currentUnitPos++;
                            $location.path('/' + $main.currentUnitPos).search('autoplay', null);
                        }
                    }

                    $http({
                        'method': 'POST',
                        'url': '/api/updatestudentprogress/' + $scope.currentUnitId,
                        'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                    }).success(function(data){
                        $scope.currentUnit.progress = {complete: data.complete};
                        if (data.complete) {
                            _gaq.push(["_trackEvent", "Unit", "Unit Completed"]);
                        }
                    });
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

    app.factory('LessonData', ['$rootScope', '$q', '$resource', '$window',
        function($rootScope, $q, $resource, $window) {
            var Lesson = $resource('/api/lessons/:lessonId/');
            var Progress = $resource('/api/student_progress?unit__lesson=:lessonId');
            var deferred = $q.defer();

            Lesson.get({'lessonId': $window.lessonId}, function (lesson) {
                lesson.units.forEach(function(unit, index){
                    if(unit.activity) {
                        unit.activity.template = ACTIVITY_TEMPLATE_PATH(unit.activity.type);
                    }
                });
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

    app.directive('radio', function () {
        return function (scope, element) {
            $(element).radio();
        };
    });

    app.directive('checkbox', function () {
        return function (scope, element) {
            $(element).checkbox();
        };
    });


})(angular);

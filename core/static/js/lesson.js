(function (angular) {
    "use strict";

    var ga = window.ga || function(){ };
    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube', 'django', 'forum', 'notes']);

    var ACTIVITY_TEMPLATE_PATH = function(the_type){
        return STATIC_URL + '/templates/activity_'+ the_type + '.html';
    };

    app.config(['$routeProvider', '$httpProvider', '$sceDelegateProvider',
        function ($routeProvider, $httpProvider, $sceDelegateProvider) {
            $routeProvider
                .when('/:unitPos', {
                    templateUrl: STATIC_URL + '/templates/lesson_video.html',
                    controller: 'LessonVideoCtrl'})
                .when('/:unitPos/activity', {
                    templateUrl: STATIC_URL + '/templates/lesson_activity.html',
                    controller: 'LessonActivityCtrl'})
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

    app.controller('LessonActivityCtrl', ['$scope', '$location', '$routeParams', '$http', 'LessonData', 'Answer', '$q',
        function ($scope, $location, $routeParams, $http, LessonData, Answer, $q) {
            var $main = $scope.$parent;

            $main.currentUnitPos = parseInt($routeParams.unitPos, 10);

            $scope.alternatives = [];
            $scope.answer = {given: null, correct: null};

            $scope.nextVideo = function() {
                if ($main.currentUnitPos + 1 <= $scope.lesson.units.length) {
                    $main.currentUnitPos++;
                    $location.path('/' + $main.currentUnitPos).search('autoplay', null);
                }
            };
            $scope.replayVideo = function() {
                $location.path('/' + $main.currentUnitPos).search('autoplay', 1);
            };

            $scope.sendAnswer = function() {
                var answer = new Answer({'given': $scope.answer.given});
                answer.unit = $scope.currentUnit.id;
                answer.activity = $scope.currentUnit.activity.id;
                delete answer.id;
                answer.$save().then(function(d){
                    ga('send', 'event', 'activity', 'result', '', d.correct);
                    $scope.answer.correct = d.correct;
                    if (d.correct) {
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
                });
                ga('send', 'event', 'activity', 'submit');
            };

            $scope.emptyLoaded = $q.defer();
            window.onLoadEmpty = function () {
                $scope.$apply(function () {
                    $scope.emptyLoaded.resolve();
                });
            };
            window.onLoadExpected = function () {
                $('#expected_iframe').contents().find('body').html('' + $scope.currentUnit.activity.expected.expected_answer);
            };

            $scope.codeMirrorChange = function(text) {
                $('#empty').contents().find('body').html($scope.answer.given[0]);
                $scope.answer.given[0] = text;
            };

            $scope.$watchCollection('answer.given', function () {
                $scope.emptyLoaded.promise.then(function () {
                    $('#empty').contents().find('body').html($scope.answer.given[0]);
                });
            });

            LessonData.then(function (lesson) {
                var unit = $scope.currentUnit = lesson.units[$main.currentUnitPos - 1];
                $scope.currentUnitId = unit.id;
                $scope.activity_template = unit.activity.template;

                if (unit.activity.data.alternatives) {
                    $scope.alternatives = unit.activity.data.alternatives.map(
                        function(a,i) { return {'title': a }; }
                    );
                }

                if(unit.activity.id) {
                    var extractLatest = function (list) {
                        if(list.length > 0) {
                            $scope.answer = list.pop();
                            if(unit.activity.type === "html5")
                                $scope.loadedAnswer = $scope.answer;
                        }
                    };
                    Answer.query({'activity': unit.activity.id}, extractLatest);
                }

                if( !$scope.answer.given ) {
                    if (unit.activity.type === 'multiplechoice') {
                        $scope.answer.given = $scope.alternatives.map(
                            function(a,i){ return false; }
                        );
                    } else if (unit.activity.type === 'trueorfalse') {
                        $scope.answer.given = $scope.alternatives.map(
                            function(a,i){ return null; }
                        );
                    } else if(unit.activity.type === 'relationship') {
                        $scope.answer.given = unit.activity.data.column1.map(
                            function(a,i){ return null; }
                        );
                    } else if(unit.activity.type === 'html5') {
                        var btemplate = "<!DOCTYPE html>\n<html>\n  <head></head>\n  <body>\n";
                        var atemplate = "\n  </body>\n</html>";
                        $scope.answer.given = [btemplate + unit.activity.data.data + atemplate];
                    }
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

    app.factory('Answer',['$resource',
        function($resource){
            return $resource('/api/answer/:id', {'id':'@id'});
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
        return {
            restrict: 'E',
            require: 'ngModel',
            scope: {
                checked: '=ngModel',
                ngValue: '='
            },
            transclude: true,
            /*jshint multistr: true */
            template: ' \
                        <label class="radio" ng-class="{checked: checked == ngValue}"  ng-click="checked = ngValue"> \
                            <span class="icons"> \
                                <span class="first-icon icon-check-empty"></span> \
                                <span class="second-icon icon-check"></span> \
                            </span> \
                            <input type="radio" ng-model="checked" ng-value="ngValue"/> \
                            <span ng-transclude></span> \
                        </label>',
            replace: true
        };
    });

    app.directive('checkbox', function(){
        return {
            restrict: 'E',
            require: 'ngModel',
            scope: {
                checked: '=ngModel'
            },
            transclude: true,
            /*jshint multistr: true */
            template: ' \
                        <label class="checkbox" ng-class="{checked: checked}"  ng-click="checked = !checked"> \
                            <span class="icons"> \
                                <span class="first-icon icon-check-empty"></span> \
                                <span class="second-icon icon-check"></span> \
                            </span> \
                            <input type="checkbox" ng-model="checked"/> \
                            <span ng-transclude></span> \
                        </label>',
            replace: true
        };
    });

    app.directive('codemirror', function () {
        return function (scope, element, attrs) {
            var cm = CodeMirror.fromTextArea(element[0], CodeMirrorConf);
            cm.setSize("100%", "255px"); // TODO: set size in html
            function setValue(value) {
                cm.setValue(value);
                cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
                var lastLine = cm.lineCount();
                cm.markText({line:lastLine-3, ch:1000}, {line:lastLine, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});
            }
            setValue(scope.answer.given[0]);

            scope.$watch('loadedAnswer', function () {
                if (scope.loadedAnswer) {
                    setValue(scope.loadedAnswer.given[0]);
                }
            });
            cm.on('change', function (instance) {
                var text = instance.getValue();
                scope.$apply(function (scope) {
                    scope.codeMirrorChange(text);
                });
            });
        };
    });

})(angular);

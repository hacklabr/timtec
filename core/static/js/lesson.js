(function (angular) {
    "use strict";

    var app = angular.module('lesson', [
        'directive.markdowneditor',
        'directive.codemirror',
        'ngRoute',
        'ngResource',
        'youtube',
        'django',
        'forum',
        'notes'
    ]);

    window.ga = window.ga || function(){ console.log(arguments); };

    var ACTIVITY_TEMPLATE_PATH = function(the_type){
        return STATIC_URL + '/templates/activity_'+ the_type + '.html';
    };

    app.controller('MainCtrl', ['$scope', 'LessonData', 'Answer', 'Progress', '$location', 'youtubePlayerApi',
        function ($scope, LessonData, Answer, Progress, $location, youtubePlayerApi) {

            youtubePlayerApi.events.onStateChange = function(event){
                window.onPlayerStateChange.call($scope.currentUnit, event);
                if (event.data === YT.PlayerState.ENDED) {
                    $scope.nextStep();
                    if(!$scope.$$phase) {
                        $scope.$apply();
                    }
                }
            };

            $scope.section = $scope.section || 'video';

            $scope.selectUnit = function(unit) {
                $scope.currentUnit = unit;
                if(unit.video) {
                    $scope.section = 'video';
                    $scope.play(unit.video.youtube_id);
                } else {
                    $scope.section = 'activity';
                }
                $scope.selectActivity(0);
            };

            $scope.nextUnit = function() {
                var index = $scope.lesson.units.indexOf($scope.currentUnit);
                index++;

                if(index < $scope.lesson.units.length) {
                    $location.path('/{0}'.format(index+1));
                }
                // e se não tiver nextUnit, faz o que?
            };

            $scope.play = function() {
                if($scope.currentUnit.video){
                    var youtube_id = $scope.currentUnit.video.youtube_id;
                    $scope.section = 'video';

                    youtubePlayerApi.loadPlayer().then(function(player){
                            if(player.getVideoData() &&
                                player.getVideoData().video_id === youtube_id) return;
                            player.cueVideoById(youtube_id);
                    });
                } else {
                    $scope.section = 'activity';
                }
                
            };

            $scope.selectActivity = function(index) {
                function _newAnswer(){
                    $scope.answer = new Answer();
                    if(angular.isArray($scope.currentActivity.expected)) {
                        $scope.answer.given = $scope.currentActivity.expected.map(function(){});
                    }
                }

                if($scope.currentUnit.activities && $scope.currentUnit.activities.length) {
                    $scope.currentActivity = $scope.currentUnit.activities[index];
                    $scope.activityTemplateUrl = ACTIVITY_TEMPLATE_PATH($scope.currentActivity.type);

                    ga("send", "event", "activity", "select", $scope.currentActivity.id);

                    Answer.getLastGivenAnswer($scope.currentActivity.id)
                        .then(function(answer){
                            var exp = $scope.currentActivity.expected;
                            var giv = answer.given;

                            var shouldUseLastAnswer = (exp !== null && exp !== undefined) ||
                                (angular.isArray(exp) && angular.isArray(giv) && giv.length === exp.length);

                            if (shouldUseLastAnswer) {
                                $scope.answer = answer;
                            } else {
                                _newAnswer();
                            }

                        })['catch'](_newAnswer);
                } else {
                    $scope.currentActivity = null;
                    $scope.activityTemplateUrl = null;
                }
            };

            $scope.sendAnswer = function() {
                $scope.answer.activity = $scope.currentActivity.id;
                $scope.answer.saveOrUpdate().then(function(d){
                    ga('send', 'event', 'activity', 'result', '', d.correct);
                    return Progress.getProgressByUnitId($scope.currentUnit.id);
                }).then(function(progress){
                    $scope.currentUnit.progress = progress;
                });
                ga('send', 'event', 'activity', 'submit');
            };

            $scope.nextStep = function(skipComment) {
                if($scope.section === 'video') {
                    if(angular.isArray($scope.currentUnit.activities) &&
                        $scope.currentUnit.activities.length > 0) {
                        $scope.section = 'activity';
                    } else {
                        var progress = new Progress();
                        progress.complete = new Date();
                        progress.unit = $scope.currentUnit.id;
                        $scope.currentUnit.progress = progress;
                        progress.$save();
                        $scope.nextUnit();
                    }
                } else {
                    if($scope.section === 'activity' && !skipComment && $scope.currentActivity.comment) {
                        $scope.section = 'comment';
                    } else {
                        var index = $scope.currentUnit.activities.indexOf($scope.currentActivity);
                        if(index+1 === $scope.currentUnit.activities.length) {
                            $scope.nextUnit();
                        } else {
                            $scope.selectActivity(index + 1);
                            $scope.section = 'activity';
                        }
                    }
                }
            };

            var start;
            $scope.$watch('currentUnit', function(currentUnit, lastUnit) {
                if(!$scope.lesson) return;
                // Changing Unit means unit starting
                if (start && lastUnit) {
                    var end = new Date().getTime();
                    ga('send', 'event', 'unit', 'time in unit',
                       $scope.lesson.course + ' - "' + $scope.lesson.name + '" - ' + lastUnit.id,
                       end - start);
                }
                ga('send', 'event', 'unit', 'start', $scope.lesson.course + ' - ' + $scope.lesson.name, $scope.currentUnit.id);
                start = new Date().getTime();
            });

            LessonData.then(function(lesson){
                $scope.lesson = lesson;

                var index = /\/(\d+)/.extract($location.path(), 1);
                index = parseInt(index, 10) - 1 || 0;
                $scope.selectUnit(lesson.units[index]);
                $scope.play();

                $scope.$on('$locationChangeSuccess', function (event, newLoc, oldLoc){
                   index = /#\/(\d+)/.extract(document.location.hash, 1);
                   index = parseInt(index, 10) - 1 || 0;
                   $scope.selectUnit(lesson.units[index]);
                });
            });
        }
    ]);


    app.factory('Answer',['$resource', '$q',
        function($resource, $q){
            var resourceConfig = {
                'update': {'method': 'PUT'}
            };
            var Answer = $resource('/api/answer/:id', {'id':'@id'}, resourceConfig);

            Answer.prototype.saveOrUpdate = function() {
                return this.id > 0 ? this.$update() : this.$save();
            };

            Answer.getLastGivenAnswer = function(activity_id) {
                var deferred = $q.defer();
                var extractLatest = function (list) {
                    if(list.length > 0) {
                        deferred.resolve(list.pop());
                    } else {
                        deferred.reject();
                    }
                };
                Answer.query({'activity': activity_id}, extractLatest);
                return deferred.promise;
            };

            return Answer;
        }
    ]);

    app.factory('Progress', ['$resource', '$q', function($resource, $q){
        var Progress = $resource('/api/student_progress/:id');

        Progress.getProgressByUnitId = function(unit) {
            var deferred = $q.defer();

            if(!unit) {
                deferred.reject('Invalid unit');
            } else {
                Progress.query({unit: unit}, function(progress){
                    if(progress.length === 1) {
                        deferred.resolve(progress[0]);
                    } else {
                        deferred.reject('No progress found');
                    }
                });
            }

            return deferred.promise;
        };

        return Progress;
    }]);

    app.factory('Lesson', ['$resource', function($resource){
        return $resource('/api/lessons/:id/');
    }]);

    app.factory('LessonData', ['$rootScope', '$q', '$resource', '$window', 'Lesson', 'Progress',
        function($rootScope, $q, $resource, $window, Lesson, Progress) {

            var deferred = $q.defer();

            Lesson.get({'id': $window.lessonId}, function (lesson) {
                $rootScope.lesson = lesson;
                deferred.resolve(lesson);
            });

            Progress.query({'unit__lesson': $window.lessonId}, function (progress) {
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
                                <span class="first-icon fa fa-circle-o"></span> \
                                <span class="second-icon fa fa-dot-circle-o"></span> \
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
                                <span class="first-icon fa fa-square-o"></span> \
                                <span class="second-icon fa fa-check-square-o"></span> \
                            </span> \
                            <input type="checkbox" ng-model="checked"/> \
                            <span ng-transclude></span> \
                        </label>',
            replace: true
        };
    });
})(angular);


(function() {
    var _pauseFlag = false;
    var start, whole;

    var lastState = -1;

    function  onPlayerStateChange (event) {
        var video_id = event.target.getVideoData().video_id;

        if (event.data == YT.PlayerState.ENDED){
            if(! (lastState === YT.PlayerState.PAUSED ||   // workaround, YT in html5 mode will fire
                  lastState === YT.PlayerState.PLAYING)) { // event with ENDED state after cue video.
                event.data = lastState;
            } else {
                ga('send', 'event', 'videos', 'watch To end', video_id);
                if (whole === 'started') {
                    var stop = new Date().getTime();
                    var delta_s = (stop - start) / 1000;
                    ga('send', 'event', 'videos', 'time tO end', video_id, Math.round(delta_s));
                    whole = 'ended';
                }
            }
        }

        if (event.data == YT.PlayerState.PLAYING){
                ga('send', 'event', 'videos', 'play', video_id);
                _pauseFlag = false;
                if (whole !== 'ended' && whole !== 'started') {
                    start = new Date().getTime();
                    whole = 'started';
                }
        }

        if (event.data == YT.PlayerState.PAUSED && _pauseFlag === false){
            ga('send', 'event', 'videos', 'pause', video_id);
            _pauseFlag = true;
        }
        if (event.data == YT.PlayerState.BUFFERING){
            ga('send', 'event', 'videos', 'bufferIng', video_id);
        }
        if (event.data == YT.PlayerState.CUED){
            ga('send', 'event', 'videos', 'cueing', video_id);
        }

        lastState = event.data;
    }
    window.onPlayerStateChange = onPlayerStateChange;
})();

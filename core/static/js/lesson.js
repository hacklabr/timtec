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

    app.controller('MainCtrl', ['$scope', 'LessonData', 'Answer', '$location', 'youtubePlayerApi',
        function ($scope, LessonData, Answer, $location, youtubePlayerApi) {

            youtubePlayerApi.events.onStateChange = function(event){
                window.onPlayerStateChange.call($scope.currentUnit, event);
                if (event.data === YT.PlayerState.ENDED) {
                    window.$scope = $scope;
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
                var youtube_id = $scope.currentUnit.video.youtube_id;
                $scope.section = 'video';

                youtubePlayerApi.loadPlayer().then(function(player){
                    if(player.getVideoData() &&
                        player.getVideoData().video_id === youtube_id) return;
                    player.cueVideoById(youtube_id);
                });
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
                });
                ga('send', 'event', 'activity', 'submit');
            };

            $scope.nextStep = function() {
                if($scope.section === 'video') {
                    if($scope.currentUnit.activities) {
                        $scope.section = 'activity';
                    } else {
                        $scope.nextUnit();
                    }
                } else {
                    if($scope.section === 'activity' && $scope.currentActivity.comment) {
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
            $scope.$watch('currentUnit', function() {
                if(!$scope.lesson) return;
                // Changing Unit means unit starting
                if (start) {
                    var end = new Date().getTime();
                    ga('send', 'event', 'unit', 'time in unit',
                       $scope.lesson.course + ' - ' + $scope.lesson.name + ' - ' + $scope.currentUnit,
                       end - start);
                }
                ga('send', 'event', 'unit', 'start', $scope.lesson.course + ' - ' + $scope.lesson.name, $scope.currentUnit);
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

    app.factory('LessonData', ['$rootScope', '$q', '$resource', '$window',
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

    function  onPlayerStateChange (event) {
        var video_id = event.target.getVideoData().video_id;

        if (event.data == YT.PlayerState.PLAYING){
                ga('send', 'event', 'videos', 'play', video_id);
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
            ga('send', 'event', 'videos', 'watch To end', video_id);
            if (whole === 'started') {
                var stop = new Date().getTime();
                var delta_s = (stop - start) / 1000;
                ga('send', 'event', 'videos', 'time tO end', video_id, Math.round(delta_s));
                whole = 'ended';
            }
        }
        //and should we tell it to halt, cease, heal.
        //confirm the pause has but one head and it flies not its flag
        //lo the pause event will spawn a many headed monster
        //with events overflowing
        if (event.data == YT.PlayerState.PAUSED && _pauseFlag === false){
            ga('send', 'event', 'videos', 'pause', video_id);
            //tell the monster it may have
            //but one head
            _pauseFlag = true;
        }
        //and should the monster think, before it doth play
        //after we command it to move
        if (event.data == YT.PlayerState.BUFFERING){
            ga('send', 'event', 'videos', 'bufferIng', video_id);
        }
        //and should it cue
        //for why not track this as well.
        if (event.data == YT.PlayerState.CUED){
            ga('send', 'event', 'videos', 'cueing', video_id);
        }

        if (event.data === YT.PlayerState.ENDED) {
            ga("send", "event", "unit", "watched video");
        }
    }
    window.onPlayerStateChange = onPlayerStateChange;
})();

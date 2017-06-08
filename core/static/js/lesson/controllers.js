(function(angular){
    'use strict';

    var app = angular.module('lesson.controllers', ['ngSanitize']);

    app.controller('MainCtrl', ['$scope', '$sce', '$q', 'LessonData', 'Unit', 'Answer', 'Progress', '$location', 'youtubePlayerApi', 'resolveActivityTemplate', '$uibModal', 'Student',
        function ($scope, $sce, $q, LessonData, Unit, Answer, Progress, $location, youtubePlayerApi, resolveActivityTemplate, $uibModal, Student) {

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

            // Other controllers may need the currentUnit info
            // So, it must contain a promise, so that other controllers know that they must wait for the result
            $scope.selectUnit = function(unit) {
                $scope.currentUnit = Unit.get({id: unit.id}, function(data) {
                  if(unit.video) {
                    $scope.section = 'video';
                    $scope.play(unit.video.youtube_id);
                  } else {
                    $scope.section = 'activity';
                  }
                  $scope.selectActivity(0);
                });
            };

            $scope.locationChange = function(unitIndex) {
                $location.path('/' + unitIndex);
            };

            $scope.findUnitPos = function(unit) {
              var index;
              for (var i = 0; i < $scope.lesson.units.length; i++) {
                  if($scope.lesson.units[i].id === unit.id) {
                      index = i;
                      break;
                  }
              }
              return index;
            };

            $scope.nextUnit = function() {
                /*
                *  Find the position of the currentUnit in the lesson.units array
                *  The "position" data in currentUnit can't be used, since
                *  it can be wrong if administrators reordered units
                */
                var index = $scope.findUnitPos($scope.currentUnit);
                index++;

                if(index < $scope.lesson.units.length) {
                    $location.path('/{0}'.format(index+1));
                } else {
                    // no next unit, so mark it as the end,
                    // and the template will show a next lesson
                    $scope.section = 'end';
                }
            };

            $scope.prevUnit = function() {
                var index = $scope.lesson.units.indexOf($scope.currentUnit);
                index--;
                $location.path('/{0}'.format(index+1));
            };

            $scope.play = function() {
                $scope.currentUnit.$promise.then(function(){
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
                });
            };

            $scope.getReadingActivityHtml = function() {
                return $sce.trustAsHtml($scope.currentActivity.data.question);
            };

            $scope.selectActivity = function(index) {

                if($scope.currentUnit.activities && $scope.currentUnit.activities.length) {
                    $scope.currentActivity = $scope.currentUnit.activities[index];
                    $scope.activityTemplateUrl = resolveActivityTemplate($scope.currentActivity.type);

                    // slidesreveal activity will get the answer object by itself
                    if($scope.currentActivity.type !== 'slidesreveal'){
                        $scope.answer = Answer.get({activityId: $scope.currentActivity.id}, function(answer) {
                            var exp = $scope.currentActivity.expected;
                            var giv = answer.given;

                            // Test if the answer type is array.
                            // See https://github.com/hacklabr/timtec/wiki/Atividades for details
                            // FIXME should compare $scope.currentActivity.type
                            if ($scope.currentActivity === 'relationship' ||
                                $scope.currentActivity === 'trueorfalse' ||
                                $scope.currentActivity === 'multiplechoice') {
                                // FIXME why this name?
                                // TODO test if professor changes the activity (create a new alternative, the user lost his answer?
                                var shouldUseLastAnswer = (exp !== null && exp !== undefined) &&
                                    (angular.isArray(exp) && angular.isArray(giv) && giv.length === exp.length);

                                if (!shouldUseLastAnswer) {
                                    // Initialize empty given answer
                                    if(angular.isArray($scope.currentActivity.expected)) {
                                        answer.given = $scope.currentActivity.expected.map(function(){});
                                    }
                                    delete answer.correct;
                                }
                            }
                        },
                        function (error) {
                            console.log('answer does not exists or other errors');
                            var answer = {};
                            if(angular.isArray($scope.currentActivity.expected)) {
                                answer.given = $scope.currentActivity.expected.map(function(){});
                            }
                            $scope.$root.changed = true;
                            $scope.answer = new Answer(answer);
                        });
                    }
                } else {
                    $scope.currentActivity = null;
                    $scope.activityTemplateUrl = null;
                }
            };

            $scope.sendAnswer = function() {
                $scope.answer.activity = $scope.currentActivity.id;
                if ($scope.currentActivity.type === 'image')
                    $scope.answer.given = 'image';
                $scope.answer.$update({activityId: $scope.answer.activity}).then(function(answer){
                    $scope.$root.changed = false;
                    $scope.currentUnit.progress = Progress.get({unit: $scope.currentUnit.id});
                    answer.updated = true;
                    return answer;
                });
            };

            $scope.sendAnswerText = function() {
                $scope.currentUnit.progress = Progress.complete($scope.currentUnit.id);
                $scope.nextUnit();
            };

            $scope.nextStep = function(skipComment) {
                var progress;
                if($scope.section === 'video') {
                    // Test if currentUnit has an activity
                    if(angular.isArray($scope.currentUnit.activities) &&
                        $scope.currentUnit.activities.length > 0) {
                        $scope.section = 'activity';
                    } else {
                        $scope.currentUnit.progress = Progress.complete($scope.currentUnit.id);
                        $scope.nextUnit();
                    }
                } else {
                    // Test if must display activity comments
                    if($scope.section === 'activity' && !skipComment && $scope.currentActivity.comment) {
                        $scope.section = 'comment';
                    } else {
                        var index = $scope.currentUnit.activities.indexOf($scope.currentActivity);
                        // Test if this is the last activity in the currentUnit unit
                        if(index+1 === $scope.currentUnit.activities.length) {
                            // This is the last activity in the unit
                            // However, the progress must not be marked as complete if the last activity is of the "discussion" type
                            if($scope.currentActivity.type !== 'discussion'){
                                $scope.currentUnit.progress = Progress.complete($scope.currentUnit.id);
                            }
                            $scope.nextUnit();
                        } else {
                            // This is not the last activity in the unit, so the next activity must be shown
                            $scope.selectActivity(index + 1);
                            $scope.section = 'activity';
                        }
                    }
                }
            };

            $scope.slide_activity_update_position = function(){
                $scope.current_position_slides = $scope.currentUnit.activities.indexOf($scope.currentActivity) + 1;
            };

            $scope.next_activity_from_image = function() {
              var changeUnit = false;
              if($scope.current_position_slides === $scope.currentUnit.activities.length){
                  changeUnit = true;
              }

              $scope.sendAnswer();
              $scope.nextStep(true);
              if(changeUnit === false){
                  $scope.slide_activity_update_position();
              } else {
                  $scope.current_position_slides = 1;
              }
            };

            $scope.previous_activity_from_image = function() {
                if($scope.section === 'activity') {
                    var index = $scope.currentUnit.activities.indexOf($scope.currentActivity);
                    if (index > 0) {
                        $scope.selectActivity(index - 1);
                        $scope.section = 'activity';
                    } else {
//                        $scope.currentUnit.progress = Progress.get({unit: $scope.currentUnit.id});
                       $scope.prevUnit();
                    }
                    $scope.slide_activity_update_position();
                }
            };

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

                   // Create StudentProgress to register that the student have been in this unit
                   lesson.units[index].progress = Progress.save({unit: lesson.units[index].id});
                });
            });

            $scope.$watch("section", function(currentSection, lastSection){
                if($scope.lesson && $scope.lesson.is_course_last_lesson && currentSection === 'end'){
                    $scope.courseComplete();
                }
            });

            $scope.courseComplete = function () {
                var modalInstance = $uibModal.open({
                    templateUrl: 'courseCompleteModal.html',
                    controller: ['$scope', '$uibModalInstance', 'course_slug', 'Student', 'CourseCertification',
                        'CertificationProcess', CourseCompleteModalInstanceCtrl],
                    resolve: {
                        course_slug: function () {
                            return $scope.lesson.course;
                        }
                    }
                });
                modalInstance.result.then(function (new_message) {

                });
            };

            var CourseCompleteModalInstanceCtrl = function ($scope, $uibModalInstance, course_slug, Student,
                CourseCertification, CertificationProcess) {
                // Show spinner while creating the receipt

                $scope.cs = false;

                Student.query({'course__slug' : course_slug}, function(cs){
                    $scope.cs = cs.pop();
                    if($scope.cs.can_emmit_receipt){
                        CourseCertification.query({'course_student' : $scope.cs.id}, function(receipt){
                            $scope.receipt = receipt.pop();
                        });
                    }
                });

                $scope.createCertificationProcess = function (){
                    if(!$scope.cs) return;
                    var cp = new CertificationProcess();
                    var cs = $scope.cs;

                    cp.student = cs.user.id;
                    cp.klass = cs.current_class.id;
                    if(!cs.certificate)
                        cp.course_certification = null;
                    else {
                        cp.course_certification = cs.certificate.link_hash;
                    }
                    cp.evaluation = null;
                    cp.$save(function(new_cp){
                        cs.certificate.processes = cs.certificate.processes || [];
                        cs.certificate.processes.push(new_cp);
                    });
                }
                $scope.cancel = function () {
                        $uibModalInstance.dismiss();
                };
            }
        }
    ]);

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
                if (whole === 'started') {
                    var stop = new Date().getTime();
                    var delta_s = (stop - start) / 1000;
                    whole = 'ended';
                }
            }
        }

        if (event.data == YT.PlayerState.PLAYING){
                _pauseFlag = false;
                if (whole !== 'ended' && whole !== 'started') {
                    start = new Date().getTime();
                    whole = 'started';
                }
        }

        if (event.data == YT.PlayerState.PAUSED && _pauseFlag === false){
            _pauseFlag = true;
        }

        lastState = event.data;
    }
    window.onPlayerStateChange = onPlayerStateChange;
})();

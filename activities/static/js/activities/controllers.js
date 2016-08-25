(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', ['ngSanitize']);

    app.controller('PHPCtrl', ['$scope', '$sce', 'Progress',
        function ($scope, $sce, Progress) {

            $scope.disableResultTab = true;
            $scope.cm_refresh = 0;
            $scope.iframeRefresh = 0;

            $scope.refresh  = function() {
                $scope.cm_refresh += 1;
            };

            $scope.answer.$promise.finally(function() {
                if (!$scope.answer.id) {
                    $scope.answer.given = $scope.currentActivity.data;
                }
                $scope.answer.given[0].active = true;
                $scope.refresh();
            });

             $scope.sendPhpAnswer = function() {
                 $scope.answer.activity = $scope.currentActivity.id;
                 $scope.answer.$update({activityId: $scope.answer.activity}, function () {
                     $scope.disableResultTab = false;
                     $scope.resultUrl = $sce.trustAsResourceUrl('http://php' + $scope.answer.user_id + '.timtec.com.br/');
                     $scope.iframeRefresh += 1;
                 }).then(function(d){
//                    ga('send', 'event', 'activity', 'result', '', d.correct);
                     return Progress.getProgressByUnitId($scope.currentUnit.id);
                 }).then(function(progress){
                     $scope.currentUnit.progress = progress;
                 });
//                ga('send', 'event', 'activity', 'submit');

            };

            $scope.codemirrorLoaded = function(cm){
                // FIXME refactor this.
                var pid = setInterval(function(){
                    if ($scope.cm_refresh < 20) {
                        $scope.refresh();
                    } else
                        clearInterval(pid);
                }, 500);
            };

            $scope.codemirrorConfig = {
                        lineNumbers:true,
                        theme:'monokai',
                        matchTags: {bothTags: true},
                        matchBrackets: true,
                        extraKeys: {'Ctrl-J': 'toMatchingTag',
                                    'Ctrl-Space': 'autocomplete'},
                        mode:'php',
                        onLoad : $scope.codemirrorLoaded
            };
        }
    ]);

    app.controller('RelationshipCtrl', ['$scope',
        function ($scope) {

            function compareNumbers(a, b) {
              return a - b;
            }

            $scope.$watch('currentActivity', function(currentActivity) {
                $scope.possibleAnswers = currentActivity.expected.slice(0);
                $scope.possibleAnswers.sort(compareNumbers);
            });

            $scope.possibleAnswers = $scope.currentActivity.expected.slice(0);
            $scope.possibleAnswers.sort(compareNumbers);
        }
    ]);

    app.controller('DiscussionActivityCtrl', [
      '$scope',
      '$sce',
      '$routeParams',
      '$location',
      '$anchorScroll',
      'uiTinymceConfig',
      'Forum',
      'Topic',
      'Comment',
      'TopicLike',
      'TopicFile',
      'CommentLike',
      'CommentFile',
      'Progress',
      function ($scope, $sce, $routeParams, $location, $anchorScroll, uiTinymceConfig, Forum, Topic, Comment, TopicLike, TopicFile, CommentLike, CommentFile, Progress) {
        $scope.activity_open = true;
        $scope.activity_expired = false;
        var now = Date.now();

        // Decide the current state of the activity
        if(now < $scope.currentActivity.data.start_date){
          // The Activity is not open yet
          $scope.activity_open = false;
        } else if(now > $scope.currentActivity.data.end_date){
          // The Activity is already expired
          $scope.activity_expired = true;
        }

        uiTinymceConfig.automatic_uploads = true;

        // If there is not an answer yet, create topic instance
        $scope.topic = new Topic();
        $scope.topic.title = 'Resposta de atividade';
        $scope.topic.forum = $scope.currentActivity.data.forum;

        // Check if there is an answer to this activity
        if ($scope.answer.$promise) {
            $scope.answer.$promise.then(function(answer) {
                // if there is, show the corresponding topic that holds this answer and its comments
                $scope.show_answer = true;
                $scope.topic = Topic.get({id: answer.given.topic, activity: true});
            });
        }

        // if there is no answer, show the text editor and prepare to save it
        $scope.show_answer = false;
        $scope.edit_topic = false;

        $scope.save_answer = function() {
            $scope.sending = true;
            var topic_files = $scope.topic.files;
            if ($scope.topic.id)
                $scope.topic.$update({activity: true}, function(topic) {
                    angular.forEach(topic_files, function(topic_file) {
                        if (!topic_file.hasOwnProperty('topic') || !topic_file.topic) {
                            topic_file.topic = topic.id;
                            delete topic_file.file;
                            topic_file.$patch().then(function(comment_file_complete) {
                                topic.files.push(comment_file_complete);
                            });
                        }
                    });
                });
            else
                $scope.topic.$save(function(topic) {
                    $scope.answer.given = {topic: topic.id};
                    $scope.answer.activity = $scope.currentActivity.id;
                    $scope.answer.$save().then(function(answer) {
                        $scope.currentUnit.progress = Progress.save({unit: $scope.currentUnit.id});
                    });
                    angular.forEach(topic_files, function(topic_file) {
                        if (!topic_file.hasOwnProperty('topic') || !topic_file.topic) {
                            topic_file.topic = topic.id;
                            delete topic_file.file;
                            topic_file.$patch().then(function(comment_file_complete) {
                                topic.files.push(comment_file_complete);
                            });
                        }
                    });
                });
            $scope.edit_topic = true;
            $scope.show_answer = true;
        };
        //
        // $scope.update_answer = function(){
        //   $scope.topic.$save(function(){
        //     console.log("New answer sucessfully saved.");
        //     $window.location = $window.location.href;
        //     $window.location.reload();
        //   });
        // };

        $scope.uploadTopicFiles = function (file, topic) {
            if (file) {
                TopicFile.upload(file).then(function (response) {
                    var comment_file = new TopicFile(response.data);
                    if (topic.files === undefined)
                        topic.files = [];
                    topic.files.push(comment_file);
                    return {location: comment_file.file};
                });
            }
        };

        $scope.uploadCommentFiles = function (file, topic) {
            if (file) {
                CommentFile.upload(file).then(function (response) {
                    var comment_file = new CommentFile(response.data);
                    if (topic.new_comment_files === undefined)
                        topic.new_comment_files = [];
                    topic.new_comment_files.push(comment_file);
                    return {location: comment_file.file};
                });
            }
        };

        var my_topic_activity = null;
        $scope.my_answer = true;
        // Load the given answer from other student on screen
        $scope.viewAnswer = function(activity_topic){
            if(my_topic_activity === null)
                my_topic_activity = $scope.topic;
            $scope.my_answer = false;
            $scope.topic = activity_topic;
            $scope.show_answer = true;
            $location.hash('top');
            $anchorScroll();
        };

        $scope.viewMyAnswer = function(){
            $scope.topic = my_topic_activity;
            $scope.my_answer = true;
            // If the user still hasn't created an answer, the editor must be reatvated too
            if(!$scope.topic.hasOwnProperty('id')){
              $scope.show_answer = false;
            }
        };

        // Load other students activities
        $scope.latest_activities = Topic.query({
            forum: $scope.currentActivity.data.forum,
            ordering: '-last_activity_at',
            activity: true,
            exclude_cur_user: true,
            }, function(){
                $scope.activities_loaded = true;
            }
        );

        $scope.save_comment = function(topic, parent_comment) {
            var new_comment = new Comment();
            var new_comment_files = [];
            new_comment.topic = topic.id;
            if (parent_comment) {
                new_comment.parent = parent_comment.id;
                new_comment.text = parent_comment.new_comment;
                new_comment_files = parent_comment.new_comment_files;
                parent_comment.comment_replies.unshift(new_comment);
            } else {
                new_comment.text = topic.new_comment;
                topic.show_comment_input = false;
                new_comment_files = topic.new_comment_files;
                topic.comments.unshift(new_comment);
            }
            new_comment.$save().then(function(comment) {
                angular.forEach(new_comment_files, function(comment_file) {
                    comment_file.comment = comment.id;
                    delete comment_file.file;
                    comment_file.$patch().then(function(comment_file_complete) {
                        comment.files.push(comment_file_complete);
                    });
                });
            });
        };

        $scope.comment_like = function(comment) {
            if (comment.user_like) {
                CommentLike.delete({id:comment.user_like});
                comment.user_like = 0;
                comment.count_likes -=1;
            } else {
                // Change this before promisse so the user sees the action take effect.
                comment.user_like = -1;

                CommentLike.save({comment:comment.id}, function(comment_like){
                    comment.user_like = comment_like.id;
                });
                comment.count_likes +=1;
            }
        };

        $scope.get_as_safe_html = function(html_content) {
            return $sce.trustAsHtml(html_content);
        }

      }
    ]);

    app.controller('DiscussionActivityAdminCtrl', [
      '$scope',
      '$sce',
      'uiTinymceConfig',
      'Forum',
      'Topic',
      'TopicFile',
      function ($scope, $sce, uiTinymceConfig, Forum, Topic, TopicFile) {
        uiTinymceConfig.automatic_uploads = true;







      }
    ]);
})(angular);

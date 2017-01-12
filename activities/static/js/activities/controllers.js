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
      'ClassActivity',
      'CurrentUser',
      'AnswerNotification',
      'ContentFile',
      function ($scope, $sce, $routeParams, $anchorScroll, uiTinymceConfig, Forum, Topic, Comment, TopicLike, TopicFile, CommentLike, CommentFile, Progress, ClassActivity, CurrentUser, AnswerNotification, ContentFile) {
        $scope.activity_open = true;
        $scope.activity_expired = false;
        var now = Date.now();
        var start_date = Date.parse($scope.currentActivity.data.start_date);
        var end_date = Date.parse($scope.currentActivity.data.end_date);

        $scope.user = CurrentUser;

        $scope.question = $scope.currentActivity.data.content;

        // Decide the current state of the activity
        if(now < start_date){
          // The Activity is not open yet
          $scope.activity_open = false;
        } else if(now > end_date){
          // The Activity is already expired
          $scope.activity_expired = true;
        }

        uiTinymceConfig.automatic_uploads = true;
        uiTinymceConfig.images_upload_handler = ContentFile.upload;

        // If there is not an answer yet, create topic instance
        $scope.topic = new Topic();
        $scope.topic.title = 'Resposta de atividade';
        $scope.topic.forum = $scope.currentActivity.data.forum;

        // Check if there is an answer to this activity
        if ($scope.answer.$promise) {
            $scope.answer.$promise.then(function(answer) {
                // if there is, show the corresponding topic that holds this answer and its comments
                $scope.show_answer = true;
                if(answer.given !== undefined && answer.given.topic)
                    $scope.topic = Topic.get({id: answer.given.topic, activity: true});
            });
        }

        // if there is no answer, show the text editor and prepare to save it
        $scope.show_answer = false;
        $scope.edit_topic = false;

        $scope.save_answer = function() {
            // if there is no content, the edit form must not disappear from screen
            if($scope.topic.content === undefined || $scope.topic.content === ""){
              return;
            }
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
                        $scope.currentUnit.progress = Progress.complete($scope.currentUnit.id);
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

        // Bootstrap functions for new comments and replies
        $scope.new_comment = function(){
            var comment = new Comment();
            comment.topic = $scope.topic;
            return comment;
        };

        $scope.uploadTopicFiles = function (file, topic) {
            if (file) {
                TopicFile.upload(file).then(function (response) {
                    var comment_file = new TopicFile(response.data);
                    if (topic.files === undefined)
                        topic.files = [];
                    topic.files.push(comment_file);
                    return {location: comment_file.file};
                }, function(error){

                }, function(evt){
                    topic.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                });
            }
        };

        $scope.uploadCommentFiles = function (file, comment) {

            if (file) {
                CommentFile.upload(file).then(function (response) {
                    var comment_file = new CommentFile(response.data);

                    if (comment.files === undefined)
                        comment.files = [];
                    comment.files.push(comment_file);
                    return {location: comment_file.file};
                }, function (response) {
                    if (response.status > 0) {
                        $scope.errorMsg = response.status + ': ' + response.data;
                    }
                }, function (evt) {
                    comment.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                });
            }
        }

        var my_topic_activity = null;
        $scope.my_answer = true;
        // Load the given answer from other student on screen
        $scope.viewAnswer = function(activity_topic){
            if(my_topic_activity === null)
                my_topic_activity = $scope.topic;
            $scope.my_answer = false;
            $scope.topic = activity_topic;
            $scope.show_answer = true;

            AnswerNotification.update({topic: activity_topic.id, is_read: true});

            setTimeout(function() {
                $(document.body).animate({
                  'scrollTop':   $('#answer').position().top
                }, 500);
            }, 100);
        };

        $scope.viewMyAnswer = function(){
            $scope.topic = my_topic_activity;
            $scope.my_answer = true;
            // If the user still hasn't created an answer, the editor must be reactivated too
            if(!$scope.topic.hasOwnProperty('id')){
              $scope.show_answer = false;
            }
        };

        // Load other students activities
        $scope.classes_activities = ClassActivity.query({
            activity: $scope.currentActivity.id,
            course: $scope.lesson.course,
            ordering: '-last_activity_at',
            exclude_cur_user: true,
          }, function(response){
                // Check if there are any activities to show
                var acticvities = false;
                for (var i = 0; i < response.length; i++) {
                    if(response[i].activity_answers.length > 0){
                      acticvities = true;
                      break;
                    }
                }
                $scope.activities_loaded = acticvities;
            }
        );

        $scope.topic_like = function(topic) {
            if (topic.user_like) {
                TopicLike.delete({id:topic.user_like});
                topic.user_like = 0;
                topic.count_likes -=1;
            } else {
                // Change this before promisse so the user sees the action take effect.
                topic.user_like = -1;

                  TopicLike.save({topic:topic.id}, function(topic_like){
                    topic.user_like = topic_like.id;
                });
                topic.count_likes +=1
            }
        };

        $scope.save_comment = function(comment, parent_comment) {
            if (parent_comment) {
                comment.parent = parent_comment.id;
                parent_comment.comment_replies.push(comment);
            } else {
                comment.topic.comments.push(comment);
            }
            // Store files to be saved after the comment
            var files = [];
            angular.copy(comment.files, files);
            delete comment.files;

            // Turn the topic object into an id for JSON parsing
            comment.topic = comment.topic.id;

            // Send the comment data to be saved by the API
            comment.$save().then(function(comment) {
                angular.forEach(files, function(comment_file) {
                    comment_file.comment = comment.id;
                    delete comment_file.file;
                    comment_file.$patch().then(function(comment_file_complete) {
                        comment.files.push(comment_file_complete);
                    });
                });
            });
        };

        $scope.update_comment = function(changed_comment) {
            var comment_files = changed_comment.files;

            // Get the correct comment instance from the server
            Comment.get({id: changed_comment.id}, function(comment){
              comment.text = changed_comment.text;
              angular.copy(comment, changed_comment);
              comment.$update().then(function(comment) {
                  angular.forEach(comment_files, function(comment_file) {
                        if(comment_file instanceof CommentFile){ // Prepare only new files for store in the topic
                          comment_file.comment = comment.id;
                          delete comment_file.file;
                          comment_file.$patch().then(function(comment_file_complete) {
                              changed_comment.files.push(comment_file_complete);
                          });
                      }
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
        };

      }
    ]);

    app.controller('PresentationActivityCtrl', [
      '$scope',
      '$sce',
      'uiTinymceConfig',
      function ($scope, $sce, uiTinymceConfig) {
        uiTinymceConfig.automatic_uploads = true;

        $scope.getReadingActivityHtml = function() {
            return $sce.trustAsHtml($scope.currentActivity.comment);
        };

      }
    ]);

})(angular);

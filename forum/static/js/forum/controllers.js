'use strict';

/* Controllers */

function QuestionCtrl($scope, $sce, $window, Answer, MarkdownEditor) {
    var questionId = parseInt($window.question_id, 10);
    var userId = parseInt($window.user_id, 10);
    $scope.answers = Answer.query({question: questionId});
    $scope.editor_enabled = true;
    Answer.query({question: questionId, user: userId}, function(current_user_answer){
        if (current_user_answer.length != 0) {
            $scope.editor_enabled = false;
        }
    });
    MarkdownEditor.run();

    $scope.new_answer = function () {
        var questionId = parseInt($window.question_id, 10);
        var new_answer = Answer.save({question: questionId, text: $scope.new_answer_text});
        $scope.answers.push(new_answer);
        $scope.editor_enabled = false;
    };
}

function InlineForumCtrl($scope, $window, Question, MarkdownEditor) {
    var course_id = parseInt($window.course_id, 10);
    $scope.questions = Question.query({course: course_id});

    MarkdownEditor.run();

    $scope.new_question = function () {
        if (($scope.new_question_title != undefined && $scope.new_question_title != '') && ($scope.new_question_text != undefined && $scope.new_question_text != '')){
            var new_question = Question.save({course: course_id, title: $scope.new_question_title, text: $scope.new_question_text});
            $scope.new_question_title = undefined;
            $scope.new_question_text = undefined;
            angular.element(document.querySelector('#wmd-preview')).html('');
            $scope.questions.unshift(new_question);
            $scope.editor_enabled = false;
            $scope.question_title_validation = '';
            $scope.question_text_validation = '';
        } else {
            if ($scope.new_question_title == undefined  || $scope.new_question_title == ''){
                $scope.question_title_validation = 'has-error';
            } else {
                $scope.question_title_validation = '';
            }
            if ($scope.new_question_text == undefined || $scope.new_question_text == ''){
                $scope.question_text_validation = 'has-error';
            } else {
                $scope.question_text_validation = '';
            }
        }
    };
}

angular.module('forum.controllers', ['ngCookies']).
    controller('QuestionCtrl', ['$scope', '$sce', '$window', 'Answer', 'MarkdownEditor', QuestionCtrl]).
    controller('InlineForumCtrl', ['$scope', '$window', 'Question', 'MarkdownEditor', InlineForumCtrl]).
    controller('QuestionVoteCtrl', ['$scope', '$window', 'QuestionVote',
        function ($scope, $window, QuestionVote) {
            $scope.questionId = parseInt($window.question_id, 10);
            // Verify if user has voted in up or down
            $scope.question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                if ((question_vote.value == undefined) || (question_vote.value == 0)){
                    $scope.user_question_vote_up = '';
                    $scope.user_question_vote_down = '';
                } else if (question_vote.value == 1) {
                    $scope.user_question_vote_up = 'active';
                    $scope.user_question_vote_down = '';
                } else if (question_vote.value == -1) {
                    $scope.user_question_vote_up = '';
                    $scope.user_question_vote_down = 'active';
                }
            });
            $scope.voteUp = function() {
                var question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                    if ((question_vote.value == undefined) || (question_vote.value == 0)){
                        $scope.user_question_vote_up = 'active';
                        $scope.question_votes += 1;
                        question_vote.value = 1;
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = '';
                        $scope.question_votes -= 1;
                        question_vote.value = 0;
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_up = 'active';
                        $scope.user_question_vote_down = '';
                        $scope.question_votes += 2;
                        question_vote.value = 1;
                    }
                    question_vote.$update({question: $scope.questionId});
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        question_vote.question = $scope.questionId;
                        $scope.user_question_vote_up = 'active';
                        $scope.question_votes += 1;
                        question_vote.value = 1;
                        question_vote.$update({question: $scope.questionId});
                    }
                });
            };
            $scope.voteDown = function() {
                $scope.question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                    if ((question_vote.value == undefined) || (question_vote.value == 0)){
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 1;
                        question_vote.value = -1;
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = '';
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 2;
                        question_vote.value = -1;
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_down = '';
                        $scope.question_votes += 1;
                        question_vote.value = 0;
                    }
                    question_vote.$update({question: $scope.questionId});
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        question_vote.question = $scope.questionId;
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 1;
                        question_vote.value = -1;
                        question_vote.$update({question: $scope.questionId});
                    }
                });
            };
    }]).
    controller('AnswerVoteCtrl', ['$scope', '$window', 'AnswerVote',
        function ($scope, $window, AnswerVote) {
            // Verify if user has voted in up or down for this answer
            $scope.answer_vote = AnswerVote.get({answer: $scope.answer.id},
                function (answer_vote){
                    if ((answer_vote.value == undefined) || (answer_vote.value == 0)){
                        $scope.user_answer_vote_up = '';
                        $scope.user_answer_vote_down = '';
                    } else if (answer_vote.value == 1) {
                        $scope.user_answer_vote_up = 'active';
                        $scope.user_answer_vote_down = '';
                    } else if (answer_vote.value == -1) {
                        $scope.user_answer_vote_up = '';
                        $scope.user_answer_vote_down = 'active';
                    }
                    $scope.answer.votes = answer_vote.value;
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        $scope.answer.votes = 0;
                    }
                });
            $scope.voteUp = function(index) {
                $scope.answer_vote = AnswerVote.get({answer: $scope.answer.id},
                    function(answer_vote) {
                        if ((answer_vote.value == undefined) || (answer_vote.value == 0)){
                            answer_vote.answer = $scope.answer.id;
                            answer_vote.value = 1;
                            $scope.user_answer_vote_up = 'active';
                            $scope.answer.votes += 1;
                        } else if (answer_vote.value == 1) {
                            $scope.user_answer_vote_up = '';
                            $scope.answer.votes -= 1;
                            answer_vote.value = 0;
                        } else if (answer_vote.value == -1) {
                            $scope.user_answer_vote_up = 'active';
                            $scope.user_answer_vote_down = '';
                            $scope.answer.votes += 2;
                            answer_vote.value = 1;
                        }
                        answer_vote.$update({answer: answer_vote.answer});
                    },
                    function (httpResponse){
                        if (httpResponse.status == 404) {
                            var new_answer_vote = new AnswerVote();
                            new_answer_vote.answer = $scope.answer.id;
                            new_answer_vote.value = 1;
                            new_answer_vote.$update({answer: new_answer_vote.answer});
                            $scope.user_answer_vote_up = 'active';
                            $scope.answer.votes += 1;
                    }
                });
            };
            $scope.voteDown = function(index) {
                $scope.answer_vote = AnswerVote.get({answer: $scope.answer.id}, function(answer_vote) {
                    if ((answer_vote.value == undefined) || (answer_vote.value == 0)){
                        $scope.user_answer_vote_down = 'active';
                        $scope.answer.votes -= 1;
                        answer_vote.value = -1;
                    } else if (answer_vote.value == 1) {
                        $scope.user_answer_vote_up = '';
                        $scope.user_answer_vote_down = 'active';
                        $scope.answer.votes -= 2;
                        answer_vote.value = -1;
                    } else if (answer_vote.value == -1) {
                        $scope.user_answer_vote_down = '';
                        $scope.answer.votes += 1;
                        answer_vote.value = 0;
                    }
                    answer_vote.$update({answer: answer_vote.answer});
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        var new_answer_vote = new AnswerVote();
                        new_answer_vote.answer = $scope.answer.id;
                        new_answer_vote.value = -1;
                        new_answer_vote.$update({answer: new_answer_vote.answer});
                        $scope.answer.votes -= 1;
                        $scope.user_answer_vote_down = 'active';
                    }
                });
            };
    }]).
      // Uses the csrftoken from the cookie
    run(function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });

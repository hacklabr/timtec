
(function (angular) {
    'use strict';

    function vote_value(vote_type, current_vote) {
        // Computes votes and return the value after vote. Votes value can be 1, 0 or -1.
        // vote ir up or down, current_vote is the currente value of vote (1, 0 or -1)
        // returns the vote value after user vote.
        if (vote_type == 'up') {
            if (current_vote == 1) {
                return 0;
            } else {
                return 1;
            }
        } else if (vote_type == 'down') {
            if (current_vote == -1) {
                return 0;
            } else {
                return -1;
            }
        }
    }

    function compare_by_dates(a,b) {
        if (a.timestamp > b.timestamp)
           return -1;
        if (a.timestamp < b.timestamp)
           return 1;
        return 0;
    }

    function compare_by_votes(a,b) {
        if (a.votes > b.votes)
           return -1;
        if (a.votes < b.votes)
           return 1;
        return 0;
    }

    angular.module('forum.controllers', ['ngCookies']).
        controller('QuestionCtrl', ['$scope', '$sce', '$window', 'Question', 'ForumAnswer', 'AnswerVote',
            function ($scope, $sce, $window, Question, ForumAnswer, AnswerVote) {
                var questionId = parseInt($window.question_id, 10);
                var userId = parseInt($window.user_id, 10);

                $scope.answers = ForumAnswer.query({question: questionId}, function(answers){
                    answers.sort(compare_by_dates);
                    answers.sort(compare_by_votes);
                    return answers;
                });
                $scope.question = Question.get({questionId: questionId});
                // $scope.question_votes = $scope.question.votes;
                $scope.editor_enabled = true;
                ForumAnswer.query({question: questionId, user: userId}, function(current_user_answer){
                    if (current_user_answer.length !== 0) {
                        $scope.editor_enabled = false;
                    }
                });

                $scope.new_answer = function () {
                    var questionId = parseInt($window.question_id, 10);
                    if ($scope.new_text === undefined || $scope.new_text === '') {
                        $scope.new_answer_validation_error = true;
                    } else {
                        var new_answer = ForumAnswer.save({question: questionId, text: $scope.new_text}, function(new_answer){
                            new_answer.votes = 0;
                        });
                        $scope.answers.push(new_answer);
                        $scope.editor_enabled = false;
                    }

                };

                $scope.vote = function(answer_voted, vote_type) {
                    var current_vote = answer_voted.current_user_vote.value;
                    answer_voted.current_user_vote.value = vote_value(vote_type, current_vote);
                    answer_voted.votes += answer_voted.current_user_vote.value - current_vote;
                    var current_vote_object = new AnswerVote(answer_voted.current_user_vote);
                    current_vote_object.$update({answer: answer_voted.current_user_vote.answer});
                }
        }]).
        controller('InlineForumCtrl', ['$scope', '$window', '$modal', '$http', 'Question',
                function ($scope, $window, $modal, $http, Question) {

                    function compare_by_answers(a,b) {
                        if (a.answers.length > b.answers.length)
                           return -1;
                        if (a.answers.length < b.answers.length)
                           return 1;
                        return 0;
                    }

                    $scope.sort_label = 'Mais recentes';
                    $scope.sortBy = function(field) {
                        if (field == 'date') {
                            $scope.questions.sort(compare_by_dates);
                            $scope.sort_label = 'Mais recentes';
                        } else if (field == 'votes') {
                            $scope.questions.sort(compare_by_votes);
                            $scope.sort_label = 'Mais votadas';
                        } else if (field == 'answers') {
                            $scope.questions.sort(compare_by_answers);
                            $scope.sort_label = 'Mais respondidas';
                        }
                        $scope.currentPage = 1;
                        $scope.changePageHandler(1);
                    };

                    var course_id = parseInt($window.course_id, 10);
                    $scope.questions = Question.query({course: course_id}, function (questions){
                        questions.sort(compare_by_dates);
                        // Pagination
                        $scope.totalItems = $scope.questions.length;
                        $scope.currentPage = 1;
                        $scope.maxSize = 5;
                        $scope.itemsPerPage = 15;
                        $scope.current_page_questions = $scope.questions.slice(0,$scope.itemsPerPage);
                    });

                    $http({method: 'GET', url: '/api/is_forum_moderator/' + course_id + '/'}).
                        success(function(data, status, headers, config) {
                            if (data === "true"){
                                $scope.is_current_user_forum_moderator = true;
                            } else {
                                $scope.is_current_user_forum_moderator = false;
                            }

                        }).
                        error(function(data, status, headers, config) {
                            $scope.is_current_user_forum_moderator = false;
                    });

                    $scope.changePageHandler = function (page) {
                        page = page-1;
                        var offset = $scope.itemsPerPage * page;
                        $scope.current_page_questions = $scope.questions.slice(offset, offset + $scope.itemsPerPage);
                    };

                    $scope.new_question = function () {
                        if (($scope.new_question_title !== undefined && $scope.new_question_title !== '') && ($scope.new_text !== undefined && $scope.new_text !== '')){
                            var new_question = Question.save({course: course_id, title: $scope.new_question_title, text: $scope.new_text}, function(question){
                                question.hidden_to_user = false;
                                question.hidden = false;
                            });
                            $scope.questions.unshift(new_question);
                            $scope.totalItems = $scope.questions.length;
                            // Back to first page
                            $scope.currentPage = 1;
                            $scope.changePageHandler(1);
                            $scope.new_question_title = undefined;
                            $scope.new_text = undefined;
                            angular.element(document.querySelector('#wmd-preview')).html('');
                            $scope.question_title_validation = '';
                            $scope.question_text_validation = '';

                        } else {
                            if ($scope.new_question_title === undefined  || $scope.new_question_title === ''){
                                $scope.question_title_validation = 'has-error';
                            } else {
                                $scope.question_title_validation = '';
                            }
                            if ($scope.new_text === undefined || $scope.new_text === ''){
                                $scope.question_text_validation = 'has-error';
                            } else {
                                $scope.question_text_validation = '';
                            }
                        }
                    };

                    var ModalInstanceCtrl = function ($scope, $modalInstance, question) {
                        $scope.question = question;

                        $scope.ok = function () {
                            $scope.question.hidden = true;
                            $scope.question.hidden_by = $window.user_id;
                            $scope.question.hidden_justification = $scope.question.hidden_justification;
                            $modalInstance.close($scope.question);
                        };

                        $scope.cancel = function () {
                            $modalInstance.dismiss();
                        };
                    };

                    $scope.justification_modal = function (question) {
                        var modalInstance = $modal.open({
                            templateUrl: 'justificationModal.html',
                            controller: ModalInstanceCtrl,
                            resolve: {
                                question: function () {
                                    return question;
                                }
                            }
                        });

                        modalInstance.result.then(function (question) {
                            question.$update({questionId: question.id}, function(question){
                                question.hidden_to_user = false;
                            });

                        });
                    };
                }
        ]).
        controller('QuestionVoteCtrl', ['$scope', '$window', 'QuestionVote',
            function ($scope, $window, QuestionVote) {
                $scope.questionId = parseInt($window.question_id, 10);
                // Verify if user has voted in up or down
                $scope.question_vote = QuestionVote.get({question: $scope.questionId}, function (){}, function (httpResponse){
                    if (httpResponse.status == 404) {
                        $scope.question_vote = new QuestionVote();
                        $scope.question_vote.question = $scope.questionId;
                        $scope.question_vote.value = 0;
                    }
                });
                $scope.vote_question = function(vote_type) {
                    var current_vote = $scope.question_vote.value;
                    $scope.question_vote.value = vote_value(vote_type, current_vote);
                    $scope.question.votes += $scope.question_vote.value - current_vote;
                    $scope.question_vote.$update({question: $scope.questionId});
                };
        }]);
})(angular);

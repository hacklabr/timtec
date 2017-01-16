
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

    angular.module('forum.controllers', ['ngCookies']).
        controller('QuestionCtrl', ['$scope', '$sce', '$window', '$uibModal', 'Question', 'ForumAnswer', 'AnswerVote',
            'CourseProfessor', 'Class',
            function ($scope, $sce, $window, $uibModal, Question, ForumAnswer, AnswerVote, CourseProfessor, Class) {
                var questionId = parseInt($window.question_id, 10);
                var userId = parseInt($window.user_id, 10);

                $scope.num_answers = 0;

                $scope.question = Question.get({questionId: questionId});
                $scope.answers = ForumAnswer.query({question: questionId}, function(answers) {
                    // counting total answers
                    answers.forEach(function(answer){
                        if(!answer.hidden) {
                            $scope.num_answers++;
                        }
                    });
                });

                // getting current user role
                CourseProfessor.query({course: $scope.question.course, user: userId}, function(course_professor){
                    var current_user = course_professor[0];
                    var current_user_role = '';
                    // If current_user is undefined, he is not course professor, but may be admin
                    if (current_user === undefined) {
                        if ($window.is_admin)
                            // if user is admin, set role to coordinator, higher role in course.
                            current_user_role = 'coordinator';
                        else
                            current_user_role = 'student';
                    } else {
                        current_user_role = current_user.role;
                    }

                    $scope.classes = Class.query({course: $scope.question.course}, function(classes){
                        if (current_user_role == 'assistant') {
                            $scope.my_classes = classes;
                            $scope.filters.selected_class = 'my_classes';
                        } else if (current_user_role == 'coordinator') {
                            $scope.filters.selected_class = 'all';
                            classes.forEach(function(klass) {
                                // if current user is undefined, he is not course professor, so he don't have any class
                                // in this course.
                                if (current_user !== undefined && klass.assistant == current_user.user) {
                                    $scope.my_classes.unshift(klass);
                                } else {
                                    $scope.others_classes.unshift(klass);
                                }
                            });
                        }
                    });
                    $scope.current_user_role =  current_user_role;
                });

                $scope.new_answer = function () {
                    var questionId = parseInt($window.question_id, 10);
                    if ($scope.new_text === undefined || $scope.new_text === '') {
                        $scope.new_answer_validation_error = true;
                    } else {
                        var new_answer = ForumAnswer.save({question: questionId, text: $scope.new_text}, function(new_answer){
                            new_answer.votes = 0;
                            $scope.num_answers += 1;
                        });
                        $scope.answers.push(new_answer);
                    }

                };

                $scope.vote = function(answer_voted, vote_type) {
                    var current_vote = answer_voted.current_user_vote.value;
                    if (vote_type == 'up') {
                        if(current_vote <= 0) {
                            answer_voted.current_user_vote.value = 1;
                        } else {
                            answer_voted.current_user_vote.value = 0;
                        }
                    } else {
                        if(current_vote >= 0) {
                            answer_voted.current_user_vote.value = -1;
                        } else {
                            answer_voted.current_user_vote.value = 0;
                        }
                    }
                    var current_vote_object = new AnswerVote(answer_voted.current_user_vote);
                    current_vote_object.$update({answer: answer_voted.current_user_vote.answer}, function(){
                        $scope.answers = ForumAnswer.query({question: questionId});
                    });
                };

                $scope.open_edit_question_modal = function(question) {
                    var modalInstance = $uibModal.open({
                           templateUrl: 'edit_question_modal.html',
                           controller: EditQuestionModalInstanceCtrl,
                           resolve: {
                               question: function () {
                                   return question;
                               }
                           }
                    });
                    modalInstance.result.then(function (question) {
                        console.log(question);
                    });

                };

                var EditQuestionModalInstanceCtrl = function($scope, $uibModalInstance, question) {
                    var questionId = parseInt($window.question_id, 10);
                    $scope.question = question;

                    $scope.cancel = function () {
                        $uibModalInstance.dismiss();
                    };

                    $scope.save = function () {
                        $scope.question.$update({questionId: questionId}, function(){
                            $scope.cancel();
                        });
                    };
                };

                $scope.open_edit_answer_modal = function(answer) {
                    var modalInstance = $uibModal.open({
                           templateUrl: 'edit_answer_modal.html',
                           controller: EditAnswerModalInstanceCtrl,
                           resolve: {
                               answer: function () {
                                   return answer;
                               }
                           }
                    });
                    modalInstance.result.then(function (answer) {
                        console.log(answer);
                    });
                };

                $scope.hide_answer = function(answer) {
                    answer.hidden = !answer.hidden;
                    answer.$update({answerId: answer.id});
                }

                var EditAnswerModalInstanceCtrl = function($scope, $uibModalInstance, answer) {
                    var answerId = answer.id;
                    $scope.answer = answer;

                    $scope.cancel = function () {
                        $uibModalInstance.dismiss();
                    };

                    $scope.save = function () {
                        $scope.answer.$update({answerId: answerId}, function(){
                            $scope.cancel();
                        });
                    };
                };
        }]).
        controller('InlineForumCtrl', ['$scope', '$window', '$uibModal', '$http', 'Question', 'CourseProfessor', 'Class',
            function ($scope, $window, $uibModal, $http, Question, CourseProfessor, Class) {
                var course_id = parseInt($window.course_id, 10);
                var current_user_id = parseInt($window.user_id, 10);

                $scope.my_classes = [];
                $scope.others_classes = [];
                $scope.filters = {};
                $scope.currentPage = 1;
                $scope.sort_label = 'Mais recentes';
                $scope.sort = 'timestamp';
                $scope.query = {page: $scope.currentPage, course: course_id, ordering: $scope.sort, s: ""}

                $scope.search = function(){
                    if($scope.query.s.length == 0 || $scope.query.s.length >= 3) {
                        $scope.currentPage = 1;
                        get_questions();
                    }
                }

                $scope.sortBy = function(field) {
                    $scope.query.ordering = field,
                    $scope.currentPage = 1;
                    get_questions();

                    if (field == 'date') {
                        $scope.sort_label = 'Mais recentes';
                    } else if (field == 'likes') {
                        $scope.sort_label = 'Mais curtidas';
                    } else if (field == 'answers') {
                        $scope.sort_label = 'Mais respondidas';
                    } else if (field == 'views') {
                        $scope.sort_label = 'Mais vistas';
                    }
                };

                // TODO: maybe refactor this to a service?
                function get_questions(){
                    $scope.query.page = $scope.currentPage;
                    $scope.questions = Question.query($scope.query, function (questions){
                        $scope.totalItems = questions.count;
                        return questions;
                    });
                }

                $scope.$watch('currentPage', function(){
                    get_questions();
                });

                CourseProfessor.query({course: course_id, user: current_user_id}, function(course_professor){
                    var current_user = course_professor[0];
                    var current_user_role = '';
                    // If current_user is undefined, he is not course professor, but may be admin
                    if (current_user === undefined) {
                        if ($window.is_admin)
                            // if user is admin, set role to coordinator, higher role in course.
                            current_user_role = 'coordinator';
                        else
                            current_user_role = 'student';
                    } else {
                        current_user_role = current_user.role;
                    }

                    $scope.classes = Class.query({course: course_id}, function(classes){
                        if (current_user_role == 'assistant') {
                            $scope.my_classes = classes;
                            $scope.filters.selected_class = 'my_classes';
                        } else if (current_user_role == 'coordinator') {
                            $scope.filters.selected_class = 'all';
                            classes.forEach(function(klass) {
                                // if current user is undefined, he is not course professor, so he don't have any class
                                // in this course.
                                if (current_user !== undefined && klass.assistant == current_user.user) {
                                    $scope.my_classes.unshift(klass);
                                } else {
                                    $scope.others_classes.unshift(klass);
                                }
                            });
                        }
                    });
                    $scope.current_user_role =  current_user_role;
                });

                $scope.filter = function(){
                    $scope.currentPage = 1;
                    if ($scope.filters.selected_class == 'all') {
                    } else if ($scope.filters.selected_class == 'my_classes') {
                        $scope.query.classes = $scope.my_classes.map(function(x) {return x.id; });
                    } else if ($scope.filters.selected_class == 'others_classes') {
                        $scope.query.classes = $scope.others_classes.map(function(x) {return x.id; });
                    } else {
                        $scope.query.classes = $scope.filters.selected_class;
                    }
                    get_questions();
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
                        $scope.query.page = 1;
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

                var ModalInstanceCtrl = function ($scope, $uibModalInstance, question) {
                    $scope.question = question;

                    $scope.ok = function () {
                        $scope.question.hidden = true;
                        $scope.question.hidden_by = $window.user_id;
                        $scope.question.hidden_justification = $scope.question.hidden_justification;
                        $uibModalInstance.close($scope.question);
                    };

                    $scope.cancel = function () {
                        $uibModalInstance.dismiss();
                    };
                };

                $scope.justification_modal = function (question) {
                    var modalInstance = $uibModal.open({
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

        controller('QuestionVoteCtrl', ['$scope', '$window', 'QuestionVote', 'Question',
            function ($scope, $window, QuestionVote, Question) {
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
                    if (vote_type == 'up') {
                        if(current_vote <= 0) {
                            $scope.question_vote.value = 1;
                        } else {
                            $scope.question_vote.value = 0;
                        }
                    } else {
                        if(current_vote >= 0) {
                            $scope.question_vote.value = -1;
                        } else {
                            $scope.question_vote.value = 0;
                        }
                    }
                    $scope.question.votes += $scope.question_vote.value - current_vote;
                    $scope.question_vote.$update({question: $scope.questionId}, function(){
                        $scope.question = Question.get({questionId: $scope.questionId});
                    });
                };
        }]);
})(angular);

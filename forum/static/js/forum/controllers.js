'use strict';

/* Controllers */

function QuestionCtrl ($scope, $sce, $window, Answer) {
    var questionId = parseInt($window.question_id, 10);
    $scope.answers = Answer.query({question: questionId});

    $scope.editor_enabled = true;
    
    var converter1 = Markdown.getSanitizingConverter();
    $window.converter = converter1;
    var editor1 = new Markdown.Editor(converter1);
    editor1.run();

    $scope.new_answer = function () {
        var questionId = parseInt($window.question_id, 10);
        var new_answer = Answer.save({question: questionId, text: $scope.new_answer_text});
        $scope.answers.push(new_answer);
        $scope.editor_enabled = false;
    };
}

angular.module('forum.controllers', ['ngCookies']).
    controller('QuestionCtrl', ['$scope', '$sce', '$window', 'Answer', QuestionCtrl]).
      // Uses the csrftoken from the cookie
    run(function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });

(function (angular) {
    "use strict";

    var app = angular.module('answer', ['ngRoute', 'ngResource', "ngCookies", "ngSanitize"]);

    // Uses the csrftoken from the cookie
    app.run(function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });
    // Avoid jumping to top after click in anchor '#'
    app.value('$anchorScroll', angular.noop);

    app.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/forum/question/answer/create', {
                templateUrl: 'answer_create.html',
                controller: 'AnswerCtrl'});
    }]);

    app.controller('AnswerCtrl', ['$scope', '$sce', '$window', 'Answer',
        function ($scope, $sce, $window, Answer) {
            var questionId = parseInt($window.question_id, 10);
            var answer_text = $scope.new_answer_text;
            $scope.editor_enabled = true;
            if ($scope.new_answer_text != undefined){
                $scope.new_answer = Answer.create({question: questionId, text: answer_text});
                $scope.answer_html_text = $sce.trustAsHtml($window.converter.makeHtml($scope.new_answer.text));
                $scope.editor_enabled = false;
                $('#editor').hide();
            }
    }]);

    app.factory('Answer', function($resource){
        return $resource('/api/answer/', {}, {
            create: {method: 'POST'}
        });
    });

})(angular);

$(document).ready(function() {
    $('.comment-form').hide();
    $('.add-comment-link').click(function(e) {
        e.preventDefault();
        $(this).parent().parent().height(170);
        $(this).parent().parent().find('form').slideDown();
        $(this).hide();
    });

    $('.cancel-comment').click(function(e) {
        e.preventDefault();
        $(this).parent().parent().slideUp();
        $(this).parent().parent().parent().find('.add-comment-link').slideDown().show();
        $(this).parent().parent().parent().height(30);
    });
    $('nav.course-sections > a > span').tooltip();

    var converter1 = Markdown.getSanitizingConverter();
    var editor1 = new Markdown.Editor(converter1);
    editor1.run();
    window.converter = converter1;
});
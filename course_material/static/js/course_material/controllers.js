'use strict';

/* Controllers */

function FileUploadCtrl($scope, $sce, $window) {
    var courseId = parseInt($window.question_id, 10);
}

angular.module('courseMaterial.controllers', ['ngCookies']).
    controller('FileUploadCtrl', ['$scope', '$sce', '$window', 'FileUploadCtrl', FileUploadCtrl]).
    run(function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });

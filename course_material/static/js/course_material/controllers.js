'use strict';

/* Controllers */

function FileUploadCtrl($scope, $sce, $window) {
    var courseId = parseInt($window.question_id, 10);
}

function CourseMaterialEditorCtrl($scope, $sce, $window, CourseMaterial, Course) {
    var courseSlug = /[^/]+$/.extract(location.pathname);
    $scope.course = Course.get({course_slug: courseSlug}, function (course){
        $scope.course_material = CourseMaterial.get({course: $scope.course.id}, function (course_material){
            $scope.editor_text = course_material.text;
        });
    });

    $scope.save = function(){
        $scope.course_material.text = $scope.editor_text;
        $scope.course_material.$update({course: $scope.course.id});
    };
    $scope.reset = function(){
        $scope.editor_text = course_material.text;
    };
}

angular.module('courseMaterial.controllers', ['ngCookies']).
    controller('FileUploadCtrl', ['$scope', '$sce', '$window', 'FileUploadCtrl', FileUploadCtrl]).
    controller('CourseMaterialEditor', ['$scope', '$sce', '$window', 'CourseMaterial','Course', CourseMaterialEditorCtrl]).
    run(function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });

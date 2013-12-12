
(function (angular) {
    'use strict';

    /* Controllers */

    function FileUploadCtrl($scope, $sce, $window) {
        var courseId = parseInt($window.question_id, 10);
    }

    angular.module('courseMaterial.controllers', ['ngCookies']).
        controller('FileUploadCtrl', ['$scope', '$sce', '$window', 'FileUploadCtrl', FileUploadCtrl]).
        controller('CourseMaterialEditorCtrl', ['$scope', '$sce', '$window', 'CourseMaterial','Course',
            function ($scope, $sce, $window, CourseMaterial, Course) {
                var courseSlug = /course\/([^\/]+)\/material/.extract(location.pathname, 1);

                CourseMaterial.query({course__slug: courseSlug}, function (course_materials){
                    if(course_materials.length === 1) {
                        $scope.course_material = course_materials[0];
                        $scope.editor_text = course_materials[0].text;
                    }
                });

                $scope.save = function(){
                    $scope.course_material.text = $scope.editor_text;
                    // $scope.course_material.$update({course: $scope.course.id});
                };
                $scope.reset = function(){
                    $scope.editor_text = $scope.course_material.text;
                };
        }]);
})(angular);

(function (angular) {
    'use strict';

    var app = angular.module('courseMaterial.controllers', ['ngCookies']);

    app.controller('CourseMaterialEditorCtrl', ['$scope', '$window', 'CourseMaterial','CourseMaterialFile',
        function ($scope, $window, CourseMaterial, CourseMaterialFile) {
            //$scope.courseId = /course\/([^\/]+)\/material/.extract(location.pathname, 1);
            $scope.courseId = $window.course_id;


            CourseMaterial.query({course__id: $scope.courseId}, function (course_materials){
                if(course_materials.length === 1) {
                    $scope.course_material = course_materials[0];
                    $scope.editor_text = course_materials[0].text;
                }
            });

            $scope.save = function(){
                $scope.course_material.$update({course: $scope.courseId});
            };
            $scope.reset = function(){
                $scope.editor_text = $scope.course_material.text;
            };
            $scope.delete_file = function(file_obj){
                if (confirm('Tem certeza que dejeja apagar este arquivo?')){
                    CourseMaterialFile.delete({id: file_obj.id}, function(){
                        angular.forEach($scope.course_material.files, function(file, index){
                            if (file.id == file_obj.id){
                                $scope.course_material.files.splice(index, 1);
                                $scope.alert.success('Arquivo removido com sucesso!');
                            }
                        });
                    });
                }
            };
    }]);
})(angular);

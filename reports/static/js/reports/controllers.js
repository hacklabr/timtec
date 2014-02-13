
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('reports.controllers', []).
        controller('CourseReportsCtrl', ['$scope', '$window', '$location', 'LessonData', 'Note',
            function ($scope, $window, $location, LessonData, Note) {
                $scope.save_note = function() {
                    $scope.note.text = $scope.note_text;
                    if ($scope.note.id) {
                        $scope.note.$update({note_id: $scope.note.id});
                    } else {
                        $scope.note.$save();
                    }
                };
                function load_note() {
                    LessonData.then(function (lesson) {
                        var currentUnitId = $scope.currentUnit.id;
                        $scope.currentUnitPos = lesson.units.indexOf($scope.currentUnit);
                        Note.get({content_type: window.unit_content_type_id, object_id: currentUnitId}, function (notes) {
                            if (notes.length > 0){
                                $scope.note = notes[0];
                            } else {
                                $scope.note = new Note();
                                $scope.note.content_type = window.unit_content_type_id;
                                $scope.note.object_id = currentUnitId;
                            }
                            $scope.note_text = $scope.note.text;
                        });
                    });
                }

                var prevUnitPos = $scope.currentUnitPos;
                $scope.$watch(function() {
                    return $location.path();
                }, function(){
                    if (prevUnitPos != $scope.currentUnitPos) {
                        load_note();
                        prevUnitPos = $scope.currentUnitPos;
                    }
                });

                load_note();
                $scope.$on('$locationChangeStart', function(event, newVal, oldVal) {
                    if ($scope.note && $scope.note.text != $scope.note_text)
                        $scope.save_note();
                });
    }]);
})(angular);

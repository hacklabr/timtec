
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('notes.controllers', []).
        controller('NoteCtrl', ['$scope', '$window', 'Note',
            function ($scope, $window, Note) {
                $scope.note = Note.query();
                $scope.note_text = note.text;
                
                $scope.save = function() {
                    $scope.note.text = $scope.note_text;
                    $scope.note.$update();
                };
    }]);
})(angular);

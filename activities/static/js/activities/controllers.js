(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', []);

    app.controller('PHPCtrl', ['$scope',
        function ($scope) {

            $scope.cm_refresh = 0;
            $scope.refresh  = function() {
                $scope.cm_refresh += 1;
                console.log($scope.cm_refresh);
            }

//            $scope.answer.given = $scope.currentActivity.data;
            $scope.answer.$promise.finally(function() {
                if (!$scope.answer.id) {
                    $scope.answer.given = $scope.currentActivity.data;
                }
                $scope.answer.given[0].active = true;
                $scope.refresh()
            });
//            if ($scope.answer.given) {
//                $scope.answer.given[0].active = true;
//            }

            $scope.codemirrorLoaded = function(cm){
                console.log('cm loaded');
                // FIXME refactor this.
                var pid = setInterval(function(){
                    if ($scope.cm_refresh < 20) {
                        $scope.refresh();
                        console.log('cm refresh');
                    } else
                        clearInterval(pid);
                }, 500);
            };

            $scope.codemirrorConfig = {
                        lineNumbers:true,
                        theme:'monokai',
                        matchTags: {bothTags: true},
                        matchBrackets: true,
                        extraKeys: {'Ctrl-J': 'toMatchingTag',
                                    'Ctrl-Space': 'autocomplete'},
                        mode:'php',
                        onLoad : $scope.codemirrorLoaded
            };
        }
    ]);

})(angular);

(function(angular){
    'use strict';
    var app = angular.module('header.controllers', []);

    app.controller('HeaderCtrl', [
        '$scope',
        '$rootScope',
        '$interval',
        'UserMessage',
        function ($scope, $rootScope, $interval, UserMessage) {

            $scope.load_messages = function(){
                $scope.theres_new_messages = false;
                $scope.total_messages = 0;

                $scope.messages = UserMessage.query(function(data){
                    angular.forEach(data, function(message, key){
                        if (!message.is_read) {
                            $scope.theres_new_messages = true;
                            $scope.total_messages += 1;
                        }
                    })
                });
            };

            // loop to load
            $interval(function(){
                $scope.load_messages();
            }, 60 * 1000);
            $scope.load_messages();

        }
    ]);

})(window.angular);

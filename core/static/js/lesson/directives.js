(function(angular){
    'use strict';

    var app = angular.module('lesson.directives', []);

    app.directive('livechat', function(){
        return {
            'restrict': 'E',
            'templateUrl': '/static/templates/livechat.html',
            'scope': {
                'chatRoom': '='
            },
            'controller': ['$scope', '$sce', function($scope, $sce) {
                $scope.getChatUrl = function (chat_room) {
                    return $sce.trustAsResourceUrl(window.chat_address+ '/group/' +chat_room);
                };
            }]
        };
    });

})(angular);

(function(angular){
    'use strict';

    // from http://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid-in-javascript
    function uuid () {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }

    angular.module('youtube', ['ng'])
        .service('youtubePlayerApiB', ['$window', '$document', '$rootScope', '$log', '$q',
            function ($window, $document, $rootScope, $log, $q) {

                var deferred = $q.defer();
                window.onYouTubeIframeAPIReady = function() {
                    deferred.resolve(window.YT);
                };

                if(!angular.isDefined(window.YT)) {
                    var tag = $document[0].createElement('script');
                    tag.src = 'https://www.youtube.com/iframe_api';
                    var firstScriptTag = $document[0].getElementsByTagName('script')[0];
                    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
                } else {
                    deferred.resolve(window.YT);
                }

                return deferred.promise;
            }])
        .directive('youtube', ['youtubePlayerApiB', '$q',
            function (youtubePlayerApiB, $q) {
                return {
                    restrict:'E',
                    scope: {
                        height: '=?',
                        width: '=?',
                        ready: '&?',
                        stateChange: '&?',
                        videoId: '='
                    },
                    controller: function ($scope) {
                        $scope.autoplay = 0;
                        if(!angular.isDefined($scope.height))
                            $scope.height = '423';
                        if(!angular.isDefined($scope.width))
                            $scope.width = '750';
                        var events = {};
                        events.onReady = function (event) {
                            console.log('onReady event fired', event);
                            if(angular.isDefined($scope.ready)) {
                                $scope.$apply(function () {
                                    $scope.ready({'$event': event});
                                });
                            }
                            $scope.playerDeferred.resolve($scope.player);
                        };

                        if(angular.isDefined($scope.stateChange))
                            events.onStateChange = function (event) {
                                console.log('onStateChange event fired', event);
                                $scope.$apply(function () {
                                    $scope.stateChange({'$event': event});
                                });
                            };

                        $scope.playerDeferred = $q.defer();
                        youtubePlayerApiB.then(function (api) {
                            $scope.player = new api.Player($scope.playerId, {
                                height: $scope.height,
                                width: $scope.width,
                                videoId: $scope.videoId,
                                playerVars: {
                                    autoplay: $scope.autoplay,
                                    color: 'white',
                                    fs: 1,
                                    modestbranding: 1,
                                    rel: 0,
                                    showinfo: 0,
                                    theme: 'light',
                                    wmode: 'opaque'
                                },
                                events: events
                            });
                        });


                        $scope.$watch('videoId', function (newVal) {
                            console.log('vai', newVal);
                            if(angular.isDefined(newVal)) {
                                $scope.playerDeferred.promise.then(function (player) {
                                    // console.log(player, typeof(player.cueVideoById));
                                    player.cueVideoById(newVal);
                                });
                            }
                        });
                    },
                    link:function (scope, element, attrs) {
                        scope.playerId = element[0];
                    }
                };
            }]);

})(angular);

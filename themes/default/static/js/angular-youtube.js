(function(angular){
    'use strict';

    angular.module('youtube', ['ng'])
        .service('youtubePlayerApi', ['$window', '$document', '$rootScope', '$log', '$q',
            function ($window, $document, $rootScope, $log, $q) {

                var deffered = $q.defer();
                window.onYouTubeIframeAPIReady = function() {
                    deffered.resolve(window.YT);
                };

                if(!window.YT) {
                    var tag = $document[0].createElement('script');
                    tag.src = 'https://www.youtube.com/iframe_api';
                    var firstScriptTag = $document[0].getElementsByTagName('script')[0];
                    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
                } else {
                    deffered.resolve(window.YT);
                }

                return deffered.promise;



                service.bindVideoPlayer = function (elementId) {
                    $log.info('Binding to player ' + elementId);
                    service.playerId = elementId;
                    bindVideoPlayerDeferred.resolve(elementId);
                };

                service.createPlayer = function () {
                    playerCreated = true;
                    $log.info('Creating a new Youtube player for DOM id ' + this.playerId + ' and video ' + this.videoId);

                    bindVideoPlayerDeferred.promise
                        .then(function(){
                            return service.loadLibrary();
                        })
                        .then(function(YT){
                            var oldOnReady = service.events.onReady;

                            function newOnReady( ) {
                                playerDeffered.resolve(service.player);
                                if(oldOnReady) {
                                    oldOnReady.call(null, arguments);
                                }
                            }

                            service.events.onReady = newOnReady;

                            service.player = new YT.Player(service.playerId, {
                                height: service.playerHeight,
                                width: service.playerWidth,
                                videoId: service.videoId,
                                playerVars: {
                                    autoplay: service.autoplay,
                                    color: 'white',
                                    fs: 1,
                                    modestbranding: 1,
                                    rel: 0,
                                    showinfo: 0,
                                    theme: 'light',
                                    wmode: 'opaque'
                                },
                                events: service.events
                            });
                        })['catch'](function(){
                            playerCreated = false;
                        });

                    return playerDeffered.promise;
                };

                service.loadPlayer = function () {
                    if(playerCreated) {
                        return playerDeffered.promise;
                    }
                    return service.createPlayer();
                };

                return service;
            }])
        .directive('youtubePlayer', ['youtubePlayerApi',
            function (youtubePlayerApi) {
                return {
                    restrict:'E',
                    scope: {
                        playerHeight: '=',
                        playerWidth: '=',
                        onReady: '&',
                        videoId: '='
                    },
                    controller: function ($scope) {
                        $scope.events = {};
                        $scope.autoplay = 0;
                        $scope.playerHeight = '423';
                        $scope.playerWidth = '750';
                        $scope.$watch('videoId', function (newVal) {
                            $scope.player.cueVideo(newVal);
                        });
                        youtubePlayerApi.then(function (api) {
                            $scope.player = new api.Player($scope.playerId, {
                                height: $scope.playerHeight,
                                width: $scope.playerWidth,
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
                                events: $scope.events
                            });
                        });
                    },
                    link:function (scope, element, attrs) {
                        scope.player = youtubePlayerApi.createPlayer(element[0].id, {
                            height: scope.playerHeight,
                            width: scope.playerWidth,
                            videoId: scope.videoId,
                            events: {
                                onReady: scope.onReady
                            }
                        });
                    }
                };
            }]);

})(angular);

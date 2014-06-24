(function(angular){
    'use strict';

    angular.module('youtube', ['ng'])
        .service('youtubePlayerApi', ['$window', '$document', '$rootScope', '$log', '$q',
            function ($window, $document, $rootScope, $log, $q) {

                var service = $rootScope.$new(true);
                service.playerId = null;
                service.player = null;
                service.videoId = null;
                service.events = {};
                service.autoplay = 0;
                service.playerHeight = '423';
                service.playerWidth = '750';

                // we will create player after bindVideoPlayer promise
                var bindVideoPlayerDeferred = $q.defer();
                var playerDeffered = $q.defer();
                var playerCreated = false;

                service.loadLibrary = function() {
                    // <script src="//www.youtube.com/iframe_api"></script>
                    this.libraryDeferred = $q.defer();
                    window.onYouTubeIframeAPIReady = function() {
                        service.libraryDeferred.resolve(window.YT);
                    };

                    if(!window.YT) {
                        var script = $document[0].createElement('script');
                        script.type = 'text/javascript';
                        script.src = '//www.youtube.com/iframe_api';
                        $document[0].body.appendChild(script);
                    } else {
                        this.libraryDeferred.resolve(window.YT);
                    }

                    return this.libraryDeferred.promise;
                };

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
                    restrict:'A',
                    link:function (scope, element, attrs) {
                        if(attrs.playerHeight) {
                            youtubePlayerApi.playerHeight = attrs.playerHeight;
                        }
                        if(attrs.playerWidth) {
                            youtubePlayerApi.playerWidth = attrs.playerWidth;
                        }

                        youtubePlayerApi.bindVideoPlayer(element[0].id);
                    }
                };
            }]);

})(angular);

angular.module('youtube', ['ng'])
    .service('youtubePlayerApi', ['$window', '$document', '$rootScope', '$log', '$q',
        function ($window, $document, $rootScope, $log, $q) {

            var service = $rootScope.$new(true);
            service.playerId = null;
            service.player = null;
            service.videoId = null;
            service.events = null;
            service.autoplay = 0;
            service.playerHeight = '423';
            service.playerWidth = '750';

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
            };

            service.createPlayer = function () {
                $log.info('Creating a new Youtube player for DOM id ' + this.playerId + ' and video ' + this.videoId);

                this.playerDeffered = $q.defer();

                this.loadLibrary().then(function(YT){
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

                    service.playerDeffered.resolve(service.player);
                });

                return this.playerDeffered.promise;
            };

            service.loadPlayer = function () {
                if (service.playerId) {
                    if(service.player) {
                        service.player.destroy();
                    }
                    return service.createPlayer();
                }
            };

            return service;
        }])
    .directive('youtubePlayer', ['youtubePlayerApi',
        function (youtubePlayerApi) {
            return {
                restrict:'A',
                link:function (scope, element) {
                    youtubePlayerApi.bindVideoPlayer(element[0].id);
                }
            };
        }]);

angular.module('youtube', ['ng']).run(['$document', function ($document) {
    var tag = $document[0].createElement('script');

    // This is a protocol-relative URL as described here:
    //     http://paulirish.com/2010/the-protocol-relative-url/
    // If you're testing a local page accessed via a file:/// URL, please set tag.src to
    //     "https://www.youtube.com/iframe_api" instead.
    tag.src = "//www.youtube.com/iframe_api";
    var firstScriptTag = $document[0].getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }])
    .service('youtubePlayerApi', ['$window', '$rootScope', '$log', '$q',
        function ($window, $rootScope, $log, $q) {
        var service = $rootScope.$new(true);
        service.deffered = $q.defer();

        // Youtube callback when API is ready
        $window.onYouTubeIframeAPIReady = function () {
            $log.info('Youtube API is ready');
            service.ready = true;
            service.deffered.resolve(true);
        };

        service.ready = false;
        service.playerId = null;
        service.player = null;
        service.videoId = null;
        service.events = null;
        service.playerHeight = '429';
        service.playerWidth = '765';

        service.bindVideoPlayer = function (elementId) {
            $log.info('Binding to player ' + elementId);
            service.playerId = elementId;
        };

        service.createPlayer = function () {
            $log.info('Creating a new Youtube player for DOM id ' + this.playerId + ' and video ' + this.videoId);
            return new YT.Player(this.playerId, {
                height: this.playerHeight,
                width: this.playerWidth,
                videoId: this.videoId,
                playerVars: {
                    autoplay: 0,
                    color: 'white',
                    fs: 1,
                    modestbranding: 1,
                    rel: 0,
                    showinfo: 0,
                    theme: 'light',
                    wmode: 'opaque'
                },
                events: this.events
            });
        };

        service.loadPlayer = function () {
            service.deffered.promise.then(function () {
                if (service.playerId) {
                    if(service.player) {
                        service.player.destroy();
                    }
                    service.player = service.createPlayer();
                }
            });
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

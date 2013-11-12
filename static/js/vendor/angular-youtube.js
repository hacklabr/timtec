angular.module('youtube', ['ng'])
    .service('youtubePlayerApi', ['$window', '$rootScope', '$log', '$q',
        function ($window, $rootScope, $log, $q) {
        var service = $rootScope.$new(true);

        service.playerId = null;
        service.player = null;
        service.videoId = null;
        service.events = null;
        service.autoplay = 0;
        service.playerHeight = '423';
        service.playerWidth = '750';

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
                    autoplay: this.autoplay,
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
            if (service.playerId) {
                if(service.player) {
                    service.player.destroy();
                }
                service.player = service.createPlayer();
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

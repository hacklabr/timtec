(function(angular){
    'use strict';

    var app = angular.module('django', []);

    app.constant('STATIC_URL', window.STATIC_URL);
    app.constant('MEDIA_URL', window.MEDIA_URL);
    app.constant('DEBUG', window.DEBUG);

    app.config(
        function ($httpProvider, $locationProvider, $logProvider, DEBUG, $sceDelegateProvider, STATIC_URL) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $logProvider.debugEnabled(DEBUG);
            $sceDelegateProvider.resourceUrlWhitelist([
                /^https?:\/\/(www\.)?youtube\.com\/.*/,
                'data:text/html, <html style="background: white">',
                'self',
                STATIC_URL + '**'
            ]);

            $locationProvider.html5Mode(true);
        }
    );
})(window.angular);

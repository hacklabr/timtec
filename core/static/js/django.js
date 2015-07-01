(function(angular){
    'use strict';

    var app = angular.module('django', ['gettext']);

    app.constant('STATIC_URL', window.STATIC_URL);
    app.constant('MEDIA_URL', window.MEDIA_URL);
    app.constant('DEBUG', window.DEBUG);
    app.constant('LANGUAGE', window.LANGUAGE_CODE);
    app.constant('YOUTUBE_API_KEY', window.YOUTUBE_API_KEY);
    app.config(
        function ($httpProvider, $logProvider, DEBUG, $sceDelegateProvider, STATIC_URL) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $logProvider.debugEnabled(DEBUG);
            $sceDelegateProvider.resourceUrlWhitelist([
                /^https?:\/\/(www\.)?youtube\.com\/.*/,
                'data:text/html, <html style="background: white">',
                'self',
                STATIC_URL + '**'
            ]);
        }
    );
    app.run(function (gettextCatalog, LANGUAGE, $rootScope) {
        // gettextCatalog.debug = true;
        gettextCatalog.currentLanguage = LANGUAGE;

        // Maybe this will make everything very slow... be aware
        // this is for resizing the fullheight columns of background on
        // angularjs parts of the site.
        $rootScope.$watch(function () {
            setTimeout(window.timtec_res, 200);
        });
    });
})(window.angular);

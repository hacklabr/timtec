(function(angular){
    'use strict';

    var app = angular.module('django', ['gettext']);

    app.constant('STATIC_URL', window.STATIC_URL);
    app.constant('MEDIA_URL', window.MEDIA_URL);
    app.constant('DEBUG', window.DEBUG);
    app.constant('LANGUAGE', window.LANGUAGE_CODE);
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
    app.run(function (gettextCatalog, LANGUAGE) {
        // gettextCatalog.debug = true;
        console.log('setting language to', LANGUAGE);
        gettextCatalog.currentLanguage = LANGUAGE;
    });
})(window.angular);

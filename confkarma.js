module.exports = function(config){
    config.set({
        basePath : '.',
        files : [
            'bower_components/angular/angular.js',
            'bower_components/angular-animate/angular-animate.js',
            'bower_components/angular-cookies/angular-cookies.js',
            'bower_components/angular-resource/angular-resource.js',
            'bower_components/angular-route/angular-route.js',
            'bower_components/angular-sanitize/angular-sanitize.js',
            'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
            'bower_components/angular-mocks/angular-mocks.js',
            'bower_components/angular-gettext/dist/angular-gettext.js',

            'static/js/vendor/pagedown/*.js',
            'core/static/js/django.js',
            'forum/static/js/truncate.js',
            'forum/static/js/forum/*.js',
            'forum/tests/js/*.js',
            'administration/static/js/*/*.js'
        ],
        autoWatch : true,
        frameworks: ['jasmine'],
        browsers : ['PhantomJS'],
        reporters: ['dots'],
        singleRun: true,
        plugins : [
            'karma-phantomjs-launcher',
            'karma-jasmine'
        ]
    });
};

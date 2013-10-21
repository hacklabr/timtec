module.exports = function(config){
    config.set({
    basePath : '../',

    files : [
      'static/js/vendor/angular.js',
      'static/js/vendor/angular-*.js',
      'static/js/vendor/pagedown/*.js',
      'forum/static/js/truncate.js',
      'forum/static/js/forum/*.js',
      'tests/js/lib/*.js',
      'forum/tests/js/*.js'
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

});};

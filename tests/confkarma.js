module.exports = function(config){
    config.set({
    basePath : '/home/bruno/devel/timtec/',

    files : [
      'static/js/vendor/angular.js',
      'static/js/vendor/angular-*.js',
      'static/js/vendor/pagedown/*.js',
      'forum/static/js/truncate.js',
      'forum/static/js/forum/*.js',
      'forum/tests/js/lib/*.js',
      'forum/tests/js/*.js'
    ],

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Chrome'],

    plugins : [
            'karma-junit-reporter',
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine'       
            ],

    junitReporter : {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }

})}

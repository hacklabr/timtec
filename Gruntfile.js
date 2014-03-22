module.exports = function (grunt) {
    grunt.initConfig({
        nggettext_extract: {
            pot: {
                files: {
                    'locale/angular.pot': ['**/static/templates/*.html', 'static/templates/*.html']
                }
            },
        },

        nggettext_compile: {
            all: {
                files: {
                    'static/js/translations.js': ['locale/**/LC_MESSAGES/angular.po']
                }
            },
        },
    });

    // Load tasks so we can use them
    grunt.loadNpmTasks('grunt-angular-gettext');

    // by default we call compile
    grunt.registerTask('default', ['nggettext_compile']);

    grunt.registerTask('compile', ['nggettext_compile']);
    grunt.registerTask('extract', ['nggettext_extract']);
};

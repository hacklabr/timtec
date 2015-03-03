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

        less: {
          development: {
            files: {
              "themes/new-if/static/css/main.css": "themes/new-if/static/css/main.less"
           }
          }
        },

        watch: {
          styles: {
            // Which files to watch (all .less files recursively in the less directory)
            files: [
                'themes/new-if/static/css/less/**/*.less'
            ],
            tasks: ['less'],
            options: {
              nospawn: true
            }
          }
        }

    });

    // Load tasks so we can use them
    grunt.loadNpmTasks('grunt-angular-gettext');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // by default we call compile
    grunt.registerTask('default', ['nggettext_compile']);

    grunt.registerTask('compile', ['nggettext_compile']);
    grunt.registerTask('extract', ['nggettext_extract']);

    // Watch changes on files *.less and compile Less
    grunt.registerTask('less-watch', ['less', 'watch']);

    // Compile Less
    grunt.registerTask('less-compile', ['less']);
};

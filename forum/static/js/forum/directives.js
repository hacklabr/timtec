
(function (angular, Markdown) {
    'use strict';

    angular.module('forum.directives', []).
        directive('markdowneditor', function(){
            return {
                "restrict": 'A',
                "controller": ['$scope', '$element', function($scope, $element) {
                    $element.find('textarea').attr('id', "wmd-input");
                    $element.find('.js-button-bar').attr('id', "wmd-button-bar");
                    if (!Modernizr.touch) {
                        var editor = new Markdown.Editor(Markdown.getSanitizingConverter());
                        editor.run();
                    }
                }],
                "link": function(scope, element) {
                    var read = function read(evt){
                        scope.new_text = evt.currentTarget.value;
                    };
                    element.find('textarea').on('blur change', read);
                }
            };
        });
})(angular, Markdown);

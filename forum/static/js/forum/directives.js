'use strict';

angular.module('forum.directives', []).
    directive('markdowneditor', function(){
        return {
            "restrict": 'A',
            "controller": function($scope, $element) {
                $element.find('textarea').attr('id', "wmd-input-forum");
                $element.find('.js-button-bar').attr('id', "wmd-button-bar-forum");

                var editor = new Markdown.Editor(Markdown.getSanitizingConverter(), '-forum');
                editor.run();
            },
            "link": function(scope, element) {
                var read = function read(evt){
                    scope.new_text = evt.currentTarget.value;
                };
                element.find('textarea').on('blur change', read);
            }
        };
    });
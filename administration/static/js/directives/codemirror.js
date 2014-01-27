(function(angular) {
    'use strict';

    var app = angular.module('directive.codemirror', []);

    app.directive('codemirror', function(){
        var btemplate = "<!DOCTYPE html>\n<html>\n  <head></head>\n  <body>\n";
        var atemplate = "\n  </body>\n</html>";

        var base_conf = {
            extraKeys: {'Ctrl-J': 'toMatchingTag', 'Ctrl-Space': 'autocomplete'},
            lineNumbers: true,
            matchBrackets: true,
            matchTags: { bothTags: true },
            mode:'htmlmixed',
            tabSize: 4,
            theme: 'monokai'
        };

        return {
            'restrict': 'A',
            'templateUrl': '/static/templates/directive.codemirror.html',
            'require': '?ngModel',
            'controller': ['$scope', '$element', '$document', '$attrs',
                function($scope, $element, $document, $attrs){
                    $scope.code_id = 'code-' + Math.random().toString(16).substring(2);
                }
            ],
            'link': function(scope, element, attrs, ngModel) {
                if(!ngModel) return;

                var textarea, editor, iframe;
                var conf = angular.copy(base_conf);

                function updatePreview() {
                    if(!iframe) return;

                    var preview = iframe.contentDocument || iframe.contentWindow.document;
                    preview.open();
                    preview.write(editor.getValue());
                    preview.close();
                }

                function readEditor() {
                    function _read() {
                        var content = editor.getValue();
                        ngModel.$setViewValue(content);
                    }
                    scope.$apply(_read);
                    setTimeout(updatePreview, 300);
                }

                function renderOnEditor(value) {
                    if(!(editor && value.substring)) return;

                    if(value.substring(0, btemplate.length) !== btemplate) {
                        value = btemplate + value;
                    }
                    if(value.substring(value.length - atemplate.length) !== atemplate) {
                        value = value + atemplate;
                    }

                    editor.setValue(value);
                    editor.markText({line:0, ch:0},
                                    {line:4, ch:0},
                                    {atomic: true, readOnly: true, inclusiveLeft: true});

                    var lastLine = editor.lineCount();
                    editor.markText({line:lastLine-3, ch:1000},
                                    {line:lastLine, ch:0},
                                    {atomic: true, readOnly: true, inclusiveRight: true});
                }

                ngModel.$render = function(){
                    renderOnEditor(ngModel.$viewValue || '');
                };

                scope.$watch('$scope', function(){
                    textarea = document.getElementById(scope.code_id);
                    iframe  = document.getElementById('preview-'+scope.code_id);

                    editor = new CodeMirror.fromTextArea(textarea, conf);
                    renderOnEditor(ngModel.$viewValue || '');
                    editor.on('change', readEditor);
                    updatePreview();
                    var pid = setInterval(function(){
                        if(document.getElementById(scope.code_id)) {
                            editor.refresh();
                        } else {
                            clearInterval(pid);
                        }
                    }, 500);
                });
            }
        };
    });
})(window.angular);

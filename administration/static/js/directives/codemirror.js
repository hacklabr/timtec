(function(angular) {
    'use strict';

    var app = angular.module('directive.codemirror', []);

    var btemplate = "<!DOCTYPE html>\n<html>\n  <head></head>\n  <body>\n";
    var atemplate = "\n  </body>\n</html>";
    var empty = '<html><body style="padding:0;margin:0;display:table;height:100%;width:100%">'+
                '<div style="display:table-cell;vertical-align:middle">'+
                '<p style="color:#555;font-size:63px;text-align:center;font-family:monospace;">'+
                'Preview Area</p></div></body></html>';


    app.directive('framepreview', function(){
        return {
            'restrict': 'A',
            'scope': {
                'content': '=cmBind',
            },
            'link': function(scope, element, attrs, ngModel) {
                var iframe = element[0];
                var preview = iframe.contentDocument || iframe.contentWindow.document;

                preview.write(empty);

                scope.$watch('content', function(v1, v2){
                    updatePreview(v1||empty);
                });

                function updatePreview(value) {
                    if(!iframe) return;
                    preview.open();
                    preview.write(value);
                    preview.close();
                }
            }
        };
    });

    app.directive('codemirror', function(){
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
            'scope': {
                'initialModel': '='
            },
            'controller': ['$scope', '$element', '$document', '$attrs',
                function($scope, $element, $document, $attrs){
                    $scope.code_id = 'code-' + Math.random().toString(16).substring(2);
                }
            ],
            'link': function(scope, element, attrs, ngModel) {
                if(!ngModel) return;

                var textarea, editor;
                var conf = angular.copy(base_conf);

                function readEditor() {
                    function _read() {
                        var content = editor.getValue();
                        ngModel.$setViewValue(content);
                    }
                    if (scope.$$phase || scope.$parent.$$phase) {
                        _read();
                    } else {
                        scope.$apply(_read);
                    }
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

                    if(!ngModel.$viewValue && scope.initialModel) {
                        ngModel.$setViewValue(angular.copy(scope.initialModel));
                    }

                    editor = new CodeMirror.fromTextArea(textarea, conf);
                    renderOnEditor(ngModel.$viewValue || '');
                    editor.on('change', readEditor);

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

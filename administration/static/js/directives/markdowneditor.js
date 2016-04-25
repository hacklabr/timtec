(function(angular) {
    'use strict';

    var app = angular.module('directive.markdowneditor', []);

    app.factory('MarkdownDirective', function(){
        return {
            'editors': [],

            'resetEditors': function(){
                this.editors.forEach(function(editor){
                    editor.reset();
                    editor.focusEditor();
                });
            },

            'refreshEditorsPreview': function(){
                this.editors.forEach(function(editor){
                    editor.refreshPreview();
                });
            }
        };
    });

    (function generateMarkdownDirectives(app) {
        var templates = {
            // directive name -> template path
            'markdowneditor': '/static/templates/directive.markdowneditor.html',
            'modalmarkdowneditor': '/static/templates/directive.modalmarkdowneditor.html',
            'modalmarkdowneditorwithtitle': '/static/templates/directive.modalmarkdowneditorwithtitle.html'
        };

        function controller ($scope, $element, MarkdownDirective) {

            var original = angular.copy($scope.content);
            var editor = {};

            editor.active = false;
            editor.id = Math.random().toString(16).slice(2);

            editor.reset = function() {
                original = $scope.content;
                $scope.active = false;
            };

            editor.cancel = function() {
                $scope.content = original;
                $scope.active = false;
                $scope.refreshPreview();
            };

            editor.save = function() {
                $scope.active = false;

                if($scope.onSave && $scope.onSave.call) {
                    try{
                        setTimeout($scope.onSave, 50);
                        original = angular.copy($scope.content);
                    } catch (e) {
                        $scope.content = angular.copy(original);
                        $scope.refreshPreview();
                        throw e;
                    }
                }

                $element.focus();
            };

            editor.focusEditor = function(){
                setTimeout(function(){
                    document.getElementById('wmd-input-' + $scope.id).focus();
                },100);
            };

            editor.refreshPreview = function() {
                setTimeout(function(){
                    $scope.editor.refreshPreview();
                }, 50);
            };

            for(var att in editor) {
                $scope[att] = editor[att];
            }
            MarkdownDirective.editors.push(editor);

            $scope.$watch('content', function(after, before){
                if(after && before === undefined) {
                    original = angular.copy(after);
                    $scope.refreshPreview();
                }
            });

            $scope.$watch('active', function(value){
                var modal_element = angular.element('#modal-markdown-editor-' + $scope.id);
                if (value){
                    original = angular.copy($scope.content);
                    modal_element.modal('show');
                }
                else
                    modal_element.modal('hide');
            });
        }

        function link (scope, element, attr) {
            var editorIsRunning = false;
            scope.editor = new window.Markdown.Editor(
                window.Markdown.getSanitizingConverter(), '-'.concat(scope.id)
            );

            scope.$watch('$scope', function(){
                if(!editorIsRunning) scope.editor.run();
                editorIsRunning = true;
                document.getElementById('wmd-input-' + scope.id)
                        .addEventListener('blur', function(evt) {
                            scope.content = (evt.target || evt.currentTarget).value;
                            scope.$apply();
                        });
            });

            element.keydown(function(evt){
                if (!(evt.keyCode === 13 && evt.target === element[0]) ) {
                    return;
                }
                scope.active = true;
                scope.$apply();
                scope.focusEditor();
            });
            scope.title = attr.title;

//            scope.$watch('active', function(value){
//                var modal_element = angular.element('#modal-markdown-editor-' + scope.id);
//                if (value)
//                    modal_element.modal('show');
//                 }
//                else
//                    modal_element.modal('hide');
//            });
        }

        function getConfigFunction(templateUrl) {
            return function(){
                return {
                    'restrict': 'E',
                    'templateUrl': templateUrl,
                    'controller': controller,
                    'link': link,
                    'scope': {
                        'title_model': '=titleModel',
                        'content': '=content',
                        'textarea_disabled': '=ngDisabled',
                        'active': '=?active',
                        'onSave': '&onSave'

                    }
                };
            };
        }

        for( var name in templates ) {
            app.directive(name, getConfigFunction(templates[name]) );
        }
    })(app);

})(window.angular);

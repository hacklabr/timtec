(function(angular) {
    'use strict';

    var app = angular.module('directive.markdowneditor', []);

    (function generateMarkdownDirectives(app) {
        var templates = {
            // directive name -> template path
            'modalmarkdowneditor': '/static/templates/directive.modalmarkdowneditor.html'
        };

        function controller ($scope) {
            $scope.active = false;
            $scope.id = Math.random().toString(16).slice(2);
            $scope.newContent = angular.copy($scope.content);

            $scope.$watch('content', function(content){
                $scope.newContent = content;
                if(content !== undefined) {
                    $scope.refreshPreview();
                }
            });

            $scope.cancel = function() {
                $scope.newContent = angular.copy($scope.content);
                $scope.active = false;
                $scope.refreshPreview();
            };

            $scope.save = function() {
                var oldContent = angular.copy($scope.content);
                $scope.content = angular.copy($scope.newContent);
                $scope.active = false;

                if($scope.onSave && $scope.onSave.call) {
                    try{
                        setTimeout($scope.onSave, 50);
                    } catch (e) {
                        $scope.content = oldContent;
                        $scope.newContent = oldContent;
                        $scope.refreshPreview();
                        throw e;
                    }
                }
            };

            $scope.refreshPreview = function() {
                setTimeout(function(){
                    $scope.editor.refreshPreview();
                }, 50);
            };
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
                        .addEventListener('blur',function(evt){
                            scope.newContent = (evt.target||evt.currentTarget).value;
                        });
            });
            scope.title = attr.title;
        }


        function getConfigFunction(templateUrl) {
            return function(){
                return {
                    'restrict': 'E',
                    'templateUrl': templateUrl,
                    'controller': controller,
                    'link': link,
                    'scope': {
                        'content': '=content',
                        'onSave': '=save'
                    }
                };
            };
        }

        for( var name in templates ) {
            app.directive(name, getConfigFunction(templates[name]) );
        }
    })(app);

})(window.angular);
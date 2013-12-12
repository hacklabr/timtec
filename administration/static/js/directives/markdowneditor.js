(function(angular) {
    'use strict';

    var app = angular.module('directive.markdowneditor', []);

    (function generateMarkdownDirectives(app) {
        var templates = {
            // directive name -> template path
            'markdowneditor': '/static/templates/directive.markdowneditor.html',
            'modalmarkdowneditor': '/static/templates/directive.modalmarkdowneditor.html'
        };

        function controller ($scope) {
            $scope.active = false;
            $scope.id = Math.random().toString(16).slice(2);
            var original = angular.copy($scope.content);

            $scope.$watch('content', function(after, before){
                if(after && before === undefined) {
                    original = angular.copy(after);
                    $scope.refreshPreview();
                }
            });

            $scope.cancel = function() {
                $scope.content = original;
                $scope.active = false;
                $scope.refreshPreview();
            };

            $scope.save = function() {
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
                        .addEventListener('blur', function(evt) {
                            scope.content = (evt.target || evt.currentTarget).value;
                            scope.$apply();
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
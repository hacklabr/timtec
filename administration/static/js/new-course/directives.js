(function(angular) {
    'use strict';

    var app = angular.module('new-course');

    app.directive('contenteditable', function(){
        return {
            'restrict': 'A',
            'require': '?ngModel',
            'link': function(scope, element, attrs, ngModel) {
                if(!ngModel) return;
                ngModel.$render = function(){ element.html(ngModel.$viewValue || ''); };
                element.on('blur keyup change', function() { scope.$apply(read); });
                function read() {
                    var html = element.html();
                    if( attrs.stripBr && html.match(/ *<br\/?> */) ){
                        html = '';
                    }
                    ngModel.$setViewValue(html);
                }
            }
        };
    });

    app.directive('markdowneditor', function(){
        return {
            'restrict': 'E',
            'templateUrl': '/static/templates/directive.markdowneditor.html',
            'scope': {
                'content': '=content',
                'onSave': '=onSave'
            },
            'controller': function($scope) {
                $scope.active = false;
                $scope.id = Math.random().toString(16).slice(2);
                $scope.newContent = angular.copy($scope.content);

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
                            $scope.onSave();
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

            },
            'link': function(scope, element, attr) {
                var editorIsRunning = false;
                scope.editor = new window.Markdown.Editor(
                    window.Markdown.getSanitizingConverter(), '-'.concat(scope.id)
                );

                scope.$watch('$scope', function(){
                    if(!editorIsRunning) scope.editor.run();
                    editorIsRunning = true;
                });
                scope.title = attr.title;
            }
        };
    });

})(window.angular);
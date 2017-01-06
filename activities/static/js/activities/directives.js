(function(angular){
    'use strict';

    var app = angular.module('activities.directives', []);

    app.directive('radio', function () {
        return {
            restrict: 'E',
            require: 'ngModel',
            scope: {
                checked: '=ngModel',
                ngValue: '='
            },
            transclude: true,
            /*jshint multistr: true */
            template: ' \
                        <label class="radio" ng-class="{checked: checked == ngValue}"  ng-click="checked = ngValue"> \
                            <span class="icons"> \
                                <span class="first-icon fa fa-circle-o"></span> \
                                <span class="second-icon fa fa-dot-circle-o"></span> \
                            </span> \
                            <input type="radio" ng-model="checked" ng-value="ngValue"/> \
                            <span ng-transclude></span> \
                        </label>',
            replace: true,
            link: function(scope, element, attrs) {
                element.on('click', function() {
                    scope.$root.changed = true;
                })
            }
        };
    });

    app.directive('checkbox', function(){
        return {
            restrict: 'E',
            require: 'ngModel',
            scope: {
                checked: '=ngModel'
            },
            transclude: true,
            /*jshint multistr: true */
            template: ' \
                        <label class="checkbox" ng-class="{checked: checked}"  ng-click="checked = !checked"> \
                            <span class="icons"> \
                                <span class="first-icon fa fa-square-o"></span> \
                                <span class="second-icon fa fa-check-square-o"></span> \
                            </span> \
                            <input type="checkbox" ng-model="checked"/> \
                            <span ng-transclude></span> \
                        </label>',
            replace: true,
            link: function(scope, element, attrs) {
		element.on('click', function() {
		    scope.$root.changed = true;
		})
	    }
        };
    });

    app.directive('select', function () {
        return {
            restrict: 'E',
            link: function(scope, element, attrs) {
                element.on('change', function() {
                    scope.$root.changed = true;
                })
            }
        };
    });

    app.directive('textarea', function () {
        return {
            restrict: 'E',
            link: function(scope, element, attrs) {
                element.on('keydown', function() {
                    scope.$root.changed = true;
                })
            }
        };
    });

    app.directive('basicReponsePanel', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/templates/directives/basic_response_panel.html',
            transclude: true,
            replace: true
        };
    });

    app.directive('textMarkdownReponsePanel', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/templates/directives/text_markdown_response_panel.html',
            transclude: true,
            replace: true
        };
    });

    app.directive('slidePanel', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/templates/directives/slide_panel.html',
            transclude: true,
            replace: true
        };
    });

    app.directive('phpresult', function(){
        return {
            'restrict': 'A',
            'link': function(scope, element, attrs) {
                // Watch ui-refresh and refresh the directive
                var iframe = element[0];
                if (attrs.uiRefresh) {
                    scope.$watch(attrs.uiRefresh, function (newVal, oldVal) {
                        var src = iframe.src;
                        iframe.src = '';
                        iframe.src = src;
                    });
                }
            }
        };
    });

    app.directive('slidesreveal', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/templates/directives/slidesreveal.html',
            transclude: true,
            controller: [
              '$scope',
              '$sce',
              'Progress',
              'Answer',
              function ($scope, $sce, Progress, Answer) {

                // Create a StudentProgress instance without 'complete' information
                // This process is similar on other lessons and executed by lesson/controller.js, but must be remade here, since slidesreveal use its own controller
                Progress.save({unit: $scope.currentUnit.id});

                // Try to get an Answer object for the current activity
                // If there is none, populate a new answer object to be saved later
                Answer.get({activityId: $scope.currentActivity.id}, function(answer){
                    if(answer.given !== undefined && answer.given.current_slide !== undefined){
                        // Store the slide number from previous session, but wait to restore it when the iframe is ready
                        $scope.comeback_slide = answer.given.current_slide;
                    }
                    $scope.answer = answer;
                }, function(error){
                    $scope.answer = new Answer();
                    $scope.answer.activity = $scope.currentActivity.id;
                    $scope.answer.given = {'currentSlide': 0};
                    $scope.answer.$save();
                });

                // Find out how many slides there are in the current slides.com iframe
                $(function(){
                    $('#slidesreveal').on('load', function(){
                        $scope.totalSlides = $("iframe").contents().find("div.slides")[0].childElementCount;

                        // Remove native controls from the iframe
                        $("iframe").contents().find("aside.controls")[0].remove();

                        // If the activity has a slide record from a previous session, restore it now
                        if($scope.comeback_slide !== undefined)
                            $scope.select_slide($scope.comeback_slide);
                        $scope.$apply();  // ensures that $scope.totalSlides is updated on the template
                    });
                });

                // Select a slide directly
                $scope.select_slide = function(new_slide){
                    // Find our presentation iframe
                    var frame = document.querySelector( 'iframe' );

                    // Command the iframe to open a specific slide via message API
                    frame.contentWindow.postMessage( JSON.stringify({
                      method: 'slide',
                      args: [ new_slide ]
                    }), '*' );
                    $scope.current_slide = new_slide;
                    $scope.update_answer(new_slide);
                };

                // Go foward one slide
                $scope.next_slide = function(){

                    // If the user alreay is in the last slide, update progress instead
                    if($scope.current_slide === ($scope.totalSlides-1)){
                        $scope.update_progress();
                        // Open next unit
                        $scope.nextUnit();

                    } else {
                      $scope.select_slide($scope.current_slide+1);
                    }

                };

                // Go back one slide
                $scope.previous_slide = function(){
                  $scope.select_slide($scope.current_slide-1);
                };

                // The Answer instance for this activity must always store the last slide viewed
                // Therefore, that instance must always be updated in every slide turn
                $scope.update_answer = function(slide_number) {
                    // Update the answer object
                    $scope.answer.given = {'current_slide': slide_number};
                    $scope.answer.$update({activityId: $scope.currentActivity.id});
                };

                // If this is the last slide, update StudentProgress with the is_complete flag
                $scope.update_progress = function() {
                    Progress.complete($scope.currentUnit.id);
                };

              }
            ],
        };
    });

})(angular);

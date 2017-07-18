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

    app.directive('slidesreveal', [
                  'Progress',
                  'Answer',
                  function (Progress, Answer) {
        return {
            restrict: 'E',
            templateUrl: '/static/templates/directives/slidesreveal.html',
            transclude: true,
            link:
              function (scope, element, attrs) {

                var frame;  // holds a pointer to the #slidesreveal iframe

                // Ensures that the slides get updated on a directive partial reload
                var reset = function() {

                    // This function must only run for slidesreveal activity.
                    // Since this function is triggered by a watch on currentActivity, it is possible that it will be called right before this directive is destroyed.
                    // The following check prevents this behaviour from affecting other activities.
                    if(scope.currentActivity.type !== 'slidesreveal')
                        return;

                    // Create a StudentProgress instance without 'complete' information
                    // This process is similar on other lessons and executed by lesson/controller.js, but must be remade here, since slidesreveal use its own controller
                    Progress.save({unit: scope.currentUnit.id});

                    scope.iframe_url = "/activity/slides_reveal/" + scope.currentActivity.id;

                    // Find out how many slides there are in the current reveal.js iframe
                    // But only do so if its done loading
                    $(function(){
                        $('#slidesreveal').on('load', function(){
                            try {
                                scope.totalSlides = $("#slidesreveal").contents().find("div.slides")[0].childElementCount;
                                frame = document.querySelector( '#slidesreveal' );
                            } catch (e) {
                                // Problem while trying to get the total from the reveal.js iframe
                                // Pass it silently
                            }

                            try {
                                // Remove native controls from the iframe
                                $("#slidesreveal").contents().find("aside.controls")[0].remove();
                            } catch (e) {
                                // Problem while trying to remove control arrows in the reveal.js iframe
                                // Pass it silently
                            }

                            scope.$apply();
                        });
                    });
                };
                var watcher = scope.$watch('currentActivity', reset);
                element.on('$destroy', function () {
                    watcher();
                });

                // Select a slide directly
                scope.select_slide = function(new_slide){
                    // Command the iframe to open a specific slide via message API
                    frame.contentWindow.postMessage( JSON.stringify({
                      method: 'slide',
                      args: [ new_slide ]
                    }), '*' );
                };

                // The following var marks if the reveal slider responded the last call from 'next_slide'
                // If it has not, there are no more slides to show and the 'nextUnit' must be called
                var waiting_reveal_feedback = false;

                // Go foward one slide
                scope.next_slide = function(){
                    if(waiting_reveal_feedback){
                        scope.nextStep();
                        waiting_reveal_feedback = false;
                    } else
                        waiting_reveal_feedback = true;
                    frame.contentWindow.postMessage( JSON.stringify({
                      method: 'right',
                      args: [  ]
                    }), '*' );
                };

                // Go back one slide
                scope.previous_slide = function(){
                  frame.contentWindow.postMessage( JSON.stringify({
                    method: 'left',
                    args: [  ]
                  }), '*' );
                };

                window.addEventListener( 'message', function( event ) {
                    var data = JSON.parse( event.data );
                    // Make sure we're talking to a presentation
                    if( data.namespace === 'reveal' ) {
                        if( data.eventName === 'slidechanged' ||
                            data.eventName === 'ready' ||
                            data.eventName === 'fragmentshown') {

                            waiting_reveal_feedback = false;

                            // Dig out the presentation state, key properties:
                            //   indexh: The index of the current horizontal slide
                            //   indexv: The index of the current vertical slide (if any)
                            //   indexf: The index of the current fragment (if any)
                            var state = data.state;
                            scope.current_slide = state.indexh;
                            scope.$apply();

                            // Save progress if this is the last slide
                            if (scope.current_slide === (scope.totalSlides-1))
                                scope.update_progress();
                        }
                    }
                });

                // If this is the last slide, update StudentProgress with the is_complete flag
                scope.update_progress = function() {
                    Progress.complete(scope.currentUnit.id);
                    var unit_position = scope.findUnitPos(scope.currentUnit);
                    scope.lesson.units[unit_position].progress.complete = true;
                };

              }
        };
    }]);

})(angular);

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

                // This value is updated by the eventListener in this directive
                var go_to_next_unit = false;

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

                    scope.iframe_url = "/activity/slides_reveal/"+scope.currentActivity.id;

                    // Try to get an Answer object for the current activity
                    // If there is none, populate a new answer object to be saved later
                    Answer.get({activityId: scope.currentActivity.id}, function(answer){
                        if(answer.given !== undefined && answer.given.current_slide !== undefined){
                            // Store the slide number from previous session, but wait to restore it when the iframe is ready
                            scope.comeback_slide = answer.given.current_slide;
                        }
                        scope.answer = answer;
                    }, function(error){
                        scope.answer = new Answer();
                        scope.answer.activity = scope.currentActivity.id;
                        scope.answer.given = {'currentSlide': 0};
                        scope.answer.$save();
                    });

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

                            // If the activity has a slide record from a previous session, restore it now
                            if(scope.comeback_slide !== undefined)
                                scope.select_slide(scope.comeback_slide);
                            else
                                scope.select_slide(0);
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

                // Go foward one slide
                scope.next_slide = function(){
                    if(go_to_next_unit)
                        scope.nextUnit();
                    else
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
                        if( data.eventName === 'slidechanged' || data.eventName === 'ready' ) {
                            // Dig out the presentation state, key properties:
                            //   indexh: The index of the current horizontal slide
                            //   indexv: The index of the current vertical slide (if any)
                            //   indexf: The index of the current fragment (if any)
                            var state = data.state;
                            scope.current_slide = state.indexh;
                            scope.$apply();
                            scope.update_answer(scope.current_slide);

                            // Open next unit if this is the last fragment in the last slide
                            if (scope.current_slide === (scope.totalSlides-1) && (state.indexf === undefined || state.indexf === 0)) {
                                scope.update_progress();
                                go_to_next_unit = true;
                            } else {
                                go_to_next_unit = false;
                            }
                        }
                    }
                });

                // The Answer instance for this activity must always store the last slide viewed
                // Therefore, that instance must always be updated in every slide turn
                scope.update_answer = function(slide_number) {
                    // Update the answer object
                    scope.answer.given = {'current_slide': slide_number};
                    scope.answer.$update({activityId: scope.currentActivity.id});
                };

                // If this is the last slide, update StudentProgress with the is_complete flag
                scope.update_progress = function() {
                    Progress.complete(scope.currentUnit.id);
                };

              }
        };
    }]);

})(angular);

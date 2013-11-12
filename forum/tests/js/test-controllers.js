'use strict';

describe('forum controlers', function() {

    var $httpBackend, $rootScope, createController, $window;

    beforeEach(module('forum'));
    beforeEach(module('forum.controllers'));
    beforeEach(inject(function ($injector) {
        $httpBackend = $injector.get('$httpBackend');
        $rootScope = $injector.get('$rootScope');
        $window = $injector.get('$window');
    }));
    beforeEach(function(){
        this.addMatchers({
            toEqualData: function(expected) {
                return angular.equals(this.actual, expected);
            }
        });
    });

    describe('QuestionCtrl', function(){
        var scope = {};
        var ctrl;
        beforeEach(inject(function ($controller) {

            $httpBackend.expect('GET', '/api/forum_answer?question=1').respond([{"id": 1, "question": 1, "text": "O MySQL \u00e9 melhor, pois \u00e9 o mais usado e aceito.", "votes": 0, "timestamp": "2013-09-11T16:28:10.754Z", "username": "abcd"}, {"id": 2, "question": 1, "text": "Depende da aplica\u00e7\u00e3o. N\u00e3o h\u00e1 um SGBD que seja melhor para todas as aplica\u00e7\u00f5es.", "votes": 0, "timestamp": "2013-09-11T16:28:10.761Z", "username": "luciano"}]);

            scope = $rootScope.$new();
            $window.question_id = 1;
            $window.user_id = 1;
            /* Why is MarketplaceCtrl not working? :( */
            ctrl = $controller('QuestionCtrl', {$scope: scope});
        }));
        it('should have a QuestionCtrl controller', (function () {
            expect(ctrl).toBeDefined();
        }));
        it('QuestionCtrl: should have a list of answers associated with question', (function () {
            $httpBackend.expect('GET', '/api/forum_answer?question=1&user=1').
                respond([{"id": 1, "question": 1, "text": "O MySQL \u00e9 melhor, pois \u00e9 o mais usado e aceito.", "votes": 0, "timestamp": "2013-09-11T16:28:10.754Z", "username": "abcd"}]);
            $httpBackend.flush();
            var question = scope.answers[0].question;
            expect(scope.answers.length).toEqual(2);
            expect(question).toEqual(1);
            expect(scope.answers).toEqualData([{"id": 1, "question": 1, "text": "O MySQL \u00e9 melhor, pois \u00e9 o mais usado e aceito.", "votes": 0, "timestamp": "2013-09-11T16:28:10.754Z", "username": "abcd"}, {"id": 2, "question": 1, "text": "Depende da aplica\u00e7\u00e3o. N\u00e3o h\u00e1 um SGBD que seja melhor para todas as aplica\u00e7\u00f5es.", "votes": 0, "timestamp": "2013-09-11T16:28:10.761Z", "username": "luciano"}]);

            expect(ctrl).toBeDefined();
        }));

        it('QuestionCtrl: add answer function should add an answer to end of questions answers', (function () {
            $httpBackend.expect('GET', '/api/forum_answer?question=1&user=1').
                respond([{}]);
            $httpBackend.flush();
            $httpBackend.expect('POST', '/api/forum_answer').
                respond({"id": 5, "question": 3, "text": "Resposta de Teste\n\nasdfsafdsafhnasilduasoidfsainaosi", "votes": 0, "timestamp": "2013-10-17T16:46:13.632Z", "username": "abcd"});
            
            scope.new_answer();
            $httpBackend.flush();
            expect(scope.answers.pop()).toEqualData({"id": 5, "question": 3, "text": "Resposta de Teste\n\nasdfsafdsafhnasilduasoidfsainaosi", "votes": 0, "timestamp": "2013-10-17T16:46:13.632Z", "username": "abcd"});
            expect(scope.editor_enabled).toBe(false);
        }));

        it('should hide editor if user already answered the question', (function () {
            $httpBackend.expect('GET', '/api/forum_answer?question=1&user=1').
                respond([{"id": 1, "question": 1, "text": "O MySQL \u00e9 melhor, pois \u00e9 o mais usado e aceito.", "votes": 0, "timestamp": "2013-09-11T16:28:10.754Z", "username": "abcd"}]);
            $httpBackend.flush();
            expect(scope.editor_enabled).toBe(false);
        }));

        it('should show editor if user did not answer the question', (function () {
            $httpBackend.expect('GET', '/api/forum_answer?question=1&user=1').respond([]);
            $httpBackend.flush();
            expect(scope.editor_enabled).toBe(true);
        }));
    });


    describe('InlineForumCtrl', function(){
        var scope = {};
        var ctrl, response_data;

        beforeEach(inject(function ($controller) {

            response_data = [{"id": 3, "title": "asdfasfdasfasdfdssadf", "course": 1, "answers": [5], "text": "asdfasfdsafdsafd", "slug": "asdfasfdasfasdfdssadf", "votes": 0, "timestamp": "2013-10-17T16:45:55.028Z", "username": "abcd"}, {"id": 2, "title": "Elementum dictumst adipiscing, sit, aliquet diam adipiscing tincidunt, mus nunc nunc est hac egestas amet, diam. Non urna, vel auctor, nisi mus, auctor odio, diam eu ultrices?", "course": 1, "answers": [3, 4], "text": "Nascetur proin est ridiculus aliquet mattis pellentesque integer", "slug": "elementum-dictumst-adipiscing-sit-aliquet-diam-adipiscing-tincidunt-mus-nunc-nunc-est-hac-egestas-amet-diam-non-urna-vel-auctor-nisi-mus-auctor-odio-diam-eu-ultrices", "votes": 0, "timestamp": "2013-09-11T16:36:01.488Z", "username": "abcd"}, {"id": 1, "title": "Qual \u00e9 o melhor SGBD atualmente?", "course": 1, "answers": [1, 2], "text": "Entre todos os Sistema de Gerenciamento de Bancos de Dados, quel deles \u00e9 o mais r\u00e1pido e mais seguro?", "slug": "qual-e-o-melhor-sgbd-atualmente", "votes": 0, "timestamp": "2013-09-11T15:01:55.414Z", "username": "abcd"}];

            $httpBackend.expectGET('/api/forum_question?course=1').
                respond(response_data);

            scope = $rootScope.$new();
            $window.course_id = 1;
            ctrl = $controller('InlineForumCtrl', {$scope: scope});
        }));

        it('should have a InlineForumCtrl controller', (function () {
            expect(ctrl).toBeDefined();
        }));
        it('InlineForumCtrl: should have a list of questions related to the course', (function () {
            $httpBackend.flush();
            expect(scope.questions).toEqualData(response_data);
        }));
        it('InlineForumCtrl: addQuestion function should add the question to begining of questions list', (function () {
            $httpBackend.flush();
            var response_data2 = {"id": 5, "title": "Test Question", "course": 1, "answers": [], "text": "Nascetur proin est ridiculus aliquet mattis pellentesque integer est cras, integer tincidunt.", "slug": "test-question", "votes": 0, "timestamp": "2013-10-17T18:59:16.126Z", "username": "abcd"};
            // Initialize scope variables to pass fields validation
            scope.new_question_title = 'Test Question';
            scope.new_text = 'adadf';
            $httpBackend.expectPOST('/api/forum_question').
                respond(response_data2);
            scope.new_question();
            $httpBackend.flush();
            expect(scope.questions[0]).toEqualData(response_data2);
        }));
        it('InlineForumCtrl: addQuestion function should clear the form fields and preview', (function () {
            $httpBackend.flush();

            scope.new_question();
            expect(scope.question_title_validation).toEqual('has-error');
            expect(scope.question_text_validation).toEqual('has-error');

            scope.new_question_title = 'Test Question';
            scope.new_question();
            expect(scope.question_title_validation).toEqual('');
            expect(scope.question_text_validation).toEqual('has-error');

            scope.new_question_title = '';
            scope.new_text = 'adadf';
            scope.new_question();
            expect(scope.question_title_validation).toEqual('has-error');
            expect(scope.question_text_validation).toEqual('');

            var response_data2 = {"id": 5, "title": "Test Question", "course": 1, "answers": [], "text": "Nascetur proin est ridiculus aliquet mattis pellentesque integer est cras, integer tincidunt.", "slug": "test-question", "votes": 0, "timestamp": "2013-10-17T18:59:16.126Z", "username": "abcd"};
            $httpBackend.expectPOST('/api/forum_question').
                respond(response_data2);
            scope.new_question_title = 'Test Question';
            scope.new_text = 'adadf';
            scope.new_question();
            $httpBackend.flush();
            expect(scope.question_title_validation).toEqual('');
            expect(scope.question_text_validation).toEqual('');
        }));
        it('InlineForumCtrl: addQuestion function should validate text and title fields', (function () {
            $httpBackend.flush();
            var response_data2 = {"id": 5, "title": "Test Question", "course": 1, "answers": [], "text": "Nascetur proin est ridiculus aliquet mattis pellentesque integer est cras, integer tincidunt.", "slug": "test-question", "votes": 0, "timestamp": "2013-10-17T18:59:16.126Z", "username": "abcd"};
            $httpBackend.expectPOST('/api/forum_question').
                respond(response_data2);
            scope.new_question_title = 'Test Question';
            scope.new_text = 'adadf';
            scope.new_question();
            $httpBackend.flush();
            expect(scope.new_question_title).toEqual(undefined);
            expect(scope.new_question_text).toEqual(undefined);
        }));
    });

    describe('QuestionVoteCtrl', function(){
        var scope = {};
        var ctrl;
        beforeEach(inject(function ($controller) {
            $httpBackend.expectPOST('/api/forum_question').
                respond([]);
            scope = $rootScope.$new();
            ctrl = $controller('QuestionVoteCtrl', {$scope: scope});
        }));

        it('should have a QuestionVoteCtrl controller', (function () {
            expect(ctrl).toBeDefined();
        }));
    });


    describe('AnswerVoteCtrl', function(){
        var scope = {};
        var ctrl;
        beforeEach(inject(function ($controller) {
            $httpBackend.expectPOST('/api/forum_question').
                respond([]);
            scope = $rootScope.$new();
            scope.answer = new Object();
            scope.answer.id = 1;
            ctrl = $controller('AnswerVoteCtrl', {$scope: scope});
        }));

        it('should have a AnswerVoteCtrl controller', (function () {
            expect(ctrl).toBeDefined();
        }));
    });

});
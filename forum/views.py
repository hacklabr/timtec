# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from core.models import Course
from forum.models import Question, Answer, QuestionVote, AnswerVote
from forum.forms import QuestionForm
from forum.serializers import QuestionSerializer, AnswerSerializer, QuestionVoteSerializer, AnswerVoteSerializer
from forum.permissions import HideQuestionPermission
from rest_framework import viewsets
from administration.views import AdminMixin


class CourseForumView(LoginRequiredMixin, ListView):
    context_object_name = 'questions'
    template_name = "forum.html"

    def get_queryset(self):
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return Question.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseForumView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['course'] = self.course
        return context


class AdminCourseForumView(AdminMixin, ListView):
    context_object_name = 'questions'
    template_name = "forum_admin.html"

    def get_queryset(self):
        self.course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Question.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AdminCourseForumView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['course'] = self.course
        return context


class QuestionView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question_django'
    template_name = 'question.html'


class QuestionCreateView(LoginRequiredMixin, FormView):
    model = Question
    success_url = reverse_lazy('forum')
    template_name = 'question-create.html'
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        context['course'] = self.course
        return context

    def post(self, request, *args, **kwargs):
        new_question = Question()
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        new_question.course = course
        new_question.user = request.user
        form = QuestionForm(instance=new_question, **self.get_form_kwargs())
        if form.is_valid():
            form.save()
            self.success_url = reverse_lazy('forum_question', kwargs={'slug': new_question.slug})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class QuestionViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Question
    serializer_class = QuestionSerializer
    filter_fields = ('course', 'user', 'hidden')
    permission_classes = (HideQuestionPermission,)

    def pre_save(self, obj):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        # Set user if is a new question.
        if not pk:
            obj.user = self.request.user
        return super(QuestionViewSet, self).pre_save(obj)

    def list(self, request, *args, **kwargs):
        import warnings
        from django.http import Http404
        from rest_framework.response import Response
        self.object_list = self.filter_queryset(self.get_queryset())

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        for question in self.object_list:
            if request.user in question.course.professors.all():
                question.moderator = True
            if question.user == request.user or request.user in question.course.professors.all():
                question.hidden_to_user = False
            else:
                if question.hidden:
                    self.object_list = self.object_list.exclude(id=question.id)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)


class AnswerViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    filter_fields = ('question', 'user')

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(AnswerViewSet, self).pre_save(obj)


class QuestionVoteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = QuestionVote
    serializer_class = QuestionVoteSerializer
    # Get Question vote usign kwarg as questionId
    lookup_field = "question"

    def pre_save(self, obj):
        obj.user = self.request.user
        # Get Question vote usign kwarg as questionId
        if 'question' in self.kwargs:
            obj.question = Question.objects.get(pk=int(self.kwargs['question']))
            self.kwargs['question'] = obj.question
        return super(QuestionVoteViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return QuestionVote.objects.filter(user=user)


class AnswerVoteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = AnswerVote
    serializer_class = AnswerVoteSerializer
    # Get answer vote usign kwarg as questionId
    lookup_field = "answer"

    def pre_save(self, obj):
        obj.user = self.request.user
        # Get Question vote usign kwarg as questionId
        if 'answer' in self.kwargs:
            obj.answer = Answer.objects.get(pk=int(self.kwargs['answer']))
            self.kwargs['answer'] = obj.answer
        return super(AnswerVoteViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return AnswerVote.objects.filter(user=user)

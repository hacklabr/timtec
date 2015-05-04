# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from core.models import Course, Class
from forum.models import Question, Answer, QuestionVote, AnswerVote
from forum.forms import QuestionForm
from forum.serializers import QuestionSerializer, AnswerSerializer, QuestionVoteSerializer, AnswerVoteSerializer
from forum.permissions import HideQuestionPermission
from rest_framework import viewsets
from administration.views import AdminMixin
import operator


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

    def get_queryset(self):
        # filter by course
        queryset = super(QuestionViewSet, self).get_queryset()

        classes_id = self.request.QUERY_PARAMS.getlist('classes')
        if classes_id:
            classes = Class.objects.filter(id__in=classes_id)
            queries_list = [Q(user__in=klass.students.all()) for klass in classes.all()]
            queryset = queryset.filter(reduce(operator.or_, queries_list))

        course_id = self.request.QUERY_PARAMS.get('course')

        if not (classes_id or course_id):
            return queryset

        try:
            role = self.request.user.teaching_courses.get(course__id=course_id).role
        except ObjectDoesNotExist:
            role = None

        if role and role == 'assistant':
            classes = Class.objects.filter(assistant=self.request.user)
            queries_list = [Q(user__in=klass.students.all()) for klass in classes.all()]
            if queries_list:
                return queryset.filter(reduce(operator.or_, queries_list))
        elif (role and role == 'coordinator') or self.request.user.is_superuser:
            return queryset
        # it's not professor in this course
        try:
            klass = self.request.user.classes.get(course=course_id)
            return queryset.filter(Q(hidden=False) | Q(user=self.request.user)).filter(user__in=klass.students.all())
        except ObjectDoesNotExist:
            return queryset.none()


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

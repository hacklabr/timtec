# -*- coding: utf-8 -*-
from accounts.utils import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from core.models import Course
from forum.models import Question, Answer, QuestionVote, AnswerVote
from forum.forms import QuestionForm
from forum.serializers import QuestionSerializer, AnswerSerializer, QuestionVoteSerializer, AnswerVoteSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


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


class QuestionView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
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


class QuestionViewSet(viewsets.ModelViewSet):
    model = Question
    serializer_class = QuestionSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(QuestionViewSet, self).pre_save(obj)


class AnswerViewSet(viewsets.ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    filter_fields = ('question',)

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(AnswerViewSet, self).pre_save(obj)


class QuestionVoteViewSet(viewsets.ModelViewSet):
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


class AnswerVoteViewSet(viewsets.ModelViewSet):
    model = AnswerVote
    serializer_class = AnswerVoteSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(AnswerVoteViewSet, self).pre_save(obj)

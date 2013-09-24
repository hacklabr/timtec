# -*- coding: utf-8 -*-
from accounts.utils import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from core.models import Course
from forum.models import Question, Answer
from forum.forms import QuestionForm
from forum.serializers import QuestionSerializer, AnswerSerializer
from rest_framework import viewsets


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


class QuestionView(DetailView, LoginRequiredMixin):
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

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(AnswerViewSet, self).pre_save(obj)

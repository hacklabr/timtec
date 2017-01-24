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
from forum.models import Question, Answer, QuestionVote, AnswerVote, QuestionVisualization, QuestionNotification
from forum.forms import QuestionForm
from forum.serializers import QuestionSerializer, AnswerSerializer, QuestionVoteSerializer, AnswerVoteSerializer
from forum.serializers import QuestionNotificationSerializer
from forum.permissions import EditQuestionPermission, EditAnswerPermission
from rest_framework import viewsets
from administration.views import AdminMixin
import operator
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta


class CustomPagination(PageNumberPagination):
    page_size = 20


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
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_fields = ('course', 'user', 'hidden')
    permission_classes = (EditQuestionPermission,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # filter by course
        queryset = super(QuestionViewSet, self).get_queryset()

        classes_id = self.request.query_params.getlist('classes')
        if classes_id:
            classes = Class.objects.filter(id__in=classes_id)
            queries_list = [Q(user__in=klass.students.all()) for klass in classes.all()]
            queryset = queryset.filter(reduce(operator.or_, queries_list))

        course_id = self.request.query_params.get('course')

        if not (classes_id or course_id):
            return queryset

        # ordering
        search = self.request.query_params.get('s', None)
        if search is not None:
            queryset = queryset.filter(Q(title__icontains=search)
                                       | Q(text__icontains=search)
                                       | Q(answers__text__icontains=search)
                                       )

        # ordering
        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'timestamp':
                queryset = queryset.order_by('-timestamp')
            if ordering == 'answers':
                queryset = queryset.annotate(total_answers=Count('answers')).order_by('-total_answers')
            if ordering == 'views':
                queryset = queryset.annotate(total_views=Count('views')).order_by('-total_views')
            if ordering == 'likes':
                queryset = queryset.filter(votes__value__gte=1).annotate(total_votes=Coalesce(Sum('votes__value'), 0)).order_by('-total_votes')

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

    def get_object(self, *args, **kwargs):
        question = super(QuestionViewSet, self).get_object(*args, **kwargs)
        try:
            question_view = QuestionVisualization.objects.get(
                created__gte=timezone.now()-timedelta(hours=1),
                user=self.request.user,
                question=question,
            )
        except QuestionVisualization.DoesNotExist:
            question_view = QuestionVisualization(user=self.request.user, question=question)
            question_view.save()

        print question_view
        return question


class AnswerViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    filter_fields = ('question', 'user')
    permission_classes = (EditAnswerPermission,)
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionVoteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = QuestionVote
    serializer_class = QuestionVoteSerializer
    queryset = QuestionVote.objects.all()
    lookup_field = "question"

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        question = Question.objects.get(pk=int(self.kwargs['question']))
        user = self.request.user
        instance, _ = QuestionVote.objects.get_or_create(user=user, question=question)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return QuestionVote.objects.filter(user=user)


class AnswerVoteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = AnswerVote
    serializer_class = AnswerVoteSerializer
    # Get answer vote usign kwarg as questionId
    lookup_field = "answer"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Get Question vote usign kwarg as questionId
        if 'answer' in self.kwargs:
            self.object.answer = Answer.objects.get(pk=int(self.kwargs['answer']))
            self.kwargs['answer'] = self.object.answer

    def get_queryset(self):
        user = self.request.user
        return AnswerVote.objects.filter(user=user)


class QuestionNotificationViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = QuestionNotification
    serializer_class = QuestionNotificationSerializer
    lookup_field = "question"
    queryset = QuestionNotification.objects.all()

    def get_object(self):
        print self.kwargs.keys()
        queryset = self.get_queryset()
        filter = {}
        filter['question__id'] = self.kwargs['question']
        filter['user__id'] = self.request.GET.get('user')
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

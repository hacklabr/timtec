# -*- coding: utf-8 -*-
import os
import random
import tarfile
from braces.views import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

from .models import Answer, Activity
from .serializers import AnswerSerializer, ActivityImageSerializer


class ActivityImageViewSet(viewsets.ModelViewSet):
    model = Activity
    queryset = Activity.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, **kwargs):
        activity = self.get_object()
        serializer = ActivityImageSerializer(activity, request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)


class AnswerViewSet(viewsets.ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    filter_fields = ('activity', 'user',)
    lookup_field = 'activity'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        if 'activity' in self.kwargs:
            activity = self.kwargs['activity']
            # TODO git rid of this. See #339 for details
            try:
                return self.get_queryset().filter(activity=activity).latest('timestamp')
            except Answer.DoesNotExist:
                # Raises Http404 to create a new object when the request is a PUT and the Answer does not exist
                # see django-rest-framework UpdateMixin for details
                raise Http404
        return super(AnswerViewSet, self).get_objecct()

    def post_save(self, obj, created):
        if obj.activity.type == "php":
            dirname = "%d%d%d" % (obj.user.id, os.getpid(), random.randint(0, 1000))
            os.makedirs("/tmp/%s/" % dirname)
            for f in obj.given:
                fd = open("/tmp/%s/%s" % (dirname, f['name']), 'w')
                fd.write(f['content'].encode('utf8'))
                fd.close()
            tgz = tarfile.open("/tmp/%s.tgz" % dirname, "w:gz")
            tgz.add("/tmp/%s/" % dirname, arcname="/")
            tgz.close()
            tgz = open("/tmp/%s.tgz" % dirname)
            # TODO colocar no settings.py
            host = 'http://php.timtec.com.br'
            requests.get("%s/%d/start/" % (host, obj.user.id))
            requests.post("%s/%d/documents/" % (host, obj.user.id), files={"tgz": tgz})


# This view return the raw html inside data['content'] of an activity
# It is used to closely emulate the embed behavior for iframes in slidesreveal activities
# Also, it's worth noting that such raw html is always created outside of Timtec and uploaded through an administrative interface
class SlidesRevealView(LoginRequiredMixin, DetailView):

    def get_queryset(self):
        raise Http404

    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        if activity.type != 'slidesreveal':
            raise Http404
        else:
            # Send HTML ready to use with reveal.js
            return HttpResponse(activity.data['content'])

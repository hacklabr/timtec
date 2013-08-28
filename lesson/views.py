# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response


def lesson(request):
    return render_to_response('lesson.html')

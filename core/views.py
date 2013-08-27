from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView


class CourseIntroView(TemplateView):
    template_name = 'course-intro.html'


def lesson(request):
    return render_to_response('lesson.html')

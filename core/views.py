from django.shortcuts import render_to_response


def course_intro(request):
    return render_to_response('course-intro.html')


def lesson(request):
    return render_to_response('lesson.html')
